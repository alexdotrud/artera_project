import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from shop.models import Artwork 

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50,  null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20,  null=False, blank=False)
    country = CountryField(blank_label='Select country')
    postcode = models.CharField(max_length=20,  null=True,  blank=True)
    town_or_city = models.CharField(max_length=40,  null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True,  blank=True)
    county = models.CharField(max_length=80,  null=True,  blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6,  decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or Decimal('0.00')
        self.order_total = total

        threshold = Decimal(getattr(settings, 'FREE_DELIVERY_THRESHOLD', 0))
        pct = Decimal(getattr(settings, 'STANDARD_DELIVERY_PERCENTAGE', 0))

        if threshold and self.order_total < threshold:
            self.delivery_cost = (self.order_total * pct / Decimal('100')).quantize(Decimal('0.01'))
        else:
            self.delivery_cost = Decimal('0.00')

        self.grand_total = (self.order_total + self.delivery_cost).quantize(Decimal('0.01'))
        self.save()

    def save(self, *args, **kwargs):
        """Set order number if not set."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    
class OrderItem(models.Model):
    order   = models.ForeignKey(Order, null=False, blank=False,
                                on_delete=models.CASCADE, related_name='lineitems')
    artwork = models.ForeignKey(Artwork, null=False, blank=False, on_delete=models.PROTECT)
    size = models.CharField(max_length=5, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2,
                                         null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Set the line item total (unit price * qty).
        Snapshot the current artwork price to avoid future price drift.
        """
        self.lineitem_total = (self.artwork.price * self.quantity).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Artwork {self.artwork.id} on order {self.order.order_number}'
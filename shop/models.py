from django.db import models
from decimal import Decimal

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

SIZE_CHOICES = [
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
]

SIZE_SURCHARGE = {
    "S": Decimal("0"),
    "M": Decimal("5"),
    "L": Decimal("10"),  # total +10 vs Small
}

class Artwork(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def price_for(self, size_code: str) -> Decimal:
        """Return base (Small) price."""
        return self.price + SIZE_SURCHARGE.get(size_code, Decimal("0"))

    def min_price(self) -> Decimal:
        """Used on listing cards: the cheapest visible price."""
        return self.price

    def __str__(self):
        return self.name
from django.db import models
from decimal import Decimal
from django.utils import timezone


SIZE_CHOICES = [
    ("S", "640x959"),
    ("M", "1280x1917"),
    ("L", "1920x2876"),
]

SIZE_SURCHARGE = {
    "S": Decimal("0"),
    "M": Decimal("5"),
    "L": Decimal("10"),
}

def calc_size_price(base_price: Decimal, size_code: str) -> Decimal:
    return (base_price + SIZE_SURCHARGE[size_code]).quantize(Decimal("0.01"))

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
    

class Artwork(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return self.name
    

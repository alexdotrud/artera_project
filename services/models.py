from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class ArtworkRequest(models.Model):
    STATUS = [
        ("in_review","In review"),
        ("accepted","Accepted"),
        ("rejected","Rejected"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_requests")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    ref_image = CloudinaryField('image', folder='requests', blank=True)
    budget_cents = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="in_review")
    created_at = models.DateTimeField(auto_now_add=True)

class Offer(models.Model):
    STATUS = [
        ("in_review","In review"),
        ("accepted","Accepted"),
        ("rejected","Rejected"),
    ]
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)
    sample_image = CloudinaryField('image', folder='requests', blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='in_review')
    created_at = models.DateTimeField(auto_now_add=True)
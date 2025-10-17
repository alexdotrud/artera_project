from django.db import models
from django.conf import settings

class ArtworkRequest(models.Model):
    STATUS = [
        ("in_review","In review"),
        ("accepted","Accepted"),
        ("rejected","Rejected"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_requests")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    ref_image_url = models.URLField(blank=True)  # keep URLs for now (you can swap to CloudinaryField later)
    budget_cents = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

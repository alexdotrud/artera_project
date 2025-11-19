from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address_line_delivery = models.CharField(max_length=255, blank=True)
    address_line_living = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = CloudinaryField('image', blank=True, null=True, folder='avatars')

    def __str__(self):
        return f"{self.user.username}'s profile"

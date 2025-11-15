from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(email_confirmed)
def make_confirmed_email_primary(request, email_address, **kwargs):
    """When a user confirms a new email, make it primary"""
    user = email_address.user
    # Make this the only primary
    EmailAddress.objects.filter(user=user).update(primary=False)
    email_address.primary = True
    email_address.save(update_fields=['primary'])

    user.email = email_address.email
    user.save(update_fields=['email'])

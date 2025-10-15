from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profile
from checkout.models import OrderItem


@login_required
def library(request):
    """All purchased artworks for the logged-in user—no pagination."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    buyer_email = (request.user.email or '').strip()
    if not buyer_email:
        buyer_email = (profile.user.email or '').strip()

    order_items = OrderItem.objects.none()
    if buyer_email:
        order_items = (
            OrderItem.objects
            .filter(order__email__iexact=buyer_email)
            .select_related('artwork', 'order')
            .order_by('-order__date', '-id')
        )

    return render(request, 'profiles/library.html', {
        'order_items': order_items,
    })
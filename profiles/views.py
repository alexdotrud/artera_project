from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Prefetch, Count

from .models import Profile
from checkout.models import OrderItem


@login_required
def library(request):
    """All orders history."""
    email = (request.user.email or '').strip()
    if not email:
        return render(request, 'profiles/library.html', {'orders': []})

    orders = (
        Order.objects
        .filter(email__iexact=email)
        .order_by('-date', '-id')
        .annotate(item_count=Count('lineitems'))
        .prefetch_related(
            Prefetch(
                'lineitems',
                queryset=OrderItem.objects.select_related('artwork').order_by('id')
            )
        )
    )
    return render(request, 'profiles/library.html', {'orders': orders})
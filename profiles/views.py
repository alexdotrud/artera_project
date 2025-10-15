from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Prefetch, Count
from django.contrib import messages

from checkout.models import OrderItem, Order
from .forms import ProfileForm
from .models import Profile

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/profile.html', {
        'form': form,
        'user_obj': request.user,
    })

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
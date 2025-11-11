from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db import transaction
from django.db.models import Prefetch, Count
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.http import HttpResponseBadRequest
import cloudinary.uploader


from checkout.models import OrderItem, Order
from .forms import ProfileForm
from .models import Profile
from services.models import ArtworkRequest

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        new_email = (request.POST.get('email') or '').strip()

        if form.is_valid():
            with transaction.atomic():
                form.save()
                if new_email and new_email.lower() != (request.user.email or '').lower():
                    # Create or reuse EmailAddress for the new email (unverified, not primary)
                    ea = EmailAddress.objects.filter(
                        user=request.user, email__iexact=new_email
                    ).first()
                    if not ea:
                        ea = EmailAddress(user=request.user, email=new_email, primary=False, verified=False)
                        ea.save()

                    # Send confirmation to the new email
                    ea.send_confirmation(request)
                    messages.info(request, "We sent a verification link to your new email. "
                                            "It will replace your current email after you confirm.")
                else:
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
def avatar_upload(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST only")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    f = request.FILES.get('avatar')
    if not f:
        return HttpResponseBadRequest("No file")

    # CloudinaryField will upload on save
    profile.avatar = f
    profile.save(update_fields=['avatar'])
    messages.success(request, "Avatar updated.")
    return redirect('profile')

@login_required
def avatar_remove(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST only")
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if profile.avatar:
        # For CloudinaryField: destroy the asset by public_id
        public_id = getattr(profile.avatar, "public_id", None)
        if public_id:
            try:
                cloudinary.uploader.destroy(public_id)
            except Exception:
                pass

        # Clear the model field
        profile.avatar = None
        profile.save(update_fields=['avatar'])

    messages.success(request, "Avatar removed.")
    return redirect('profile')

@login_required
def library(request):
    """All orders history."""
    email = (request.user.email or '').strip()
    if not email:
        return render(request, 'profiles/library.html', {'orders': []})

    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by('-date', '-id')
        .annotate(item_count=Count('lineitems'))
        .prefetch_related(
            Prefetch(
                'lineitems',
                queryset=OrderItem.objects.select_related('artwork').order_by('id')
            )
        )
    )
    requests_qs = (
        ArtworkRequest.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(request, 'profiles/library.html', {
        'orders': orders,
        'requests': requests_qs,
    })

@login_required
def download_artwork(request, order_number, lineitem_id):
    # Order must belong to the logged-in user (by email)
    order = get_object_or_404(Order, order_number=order_number)
    if not request.user.email or order.email.lower() != request.user.email.lower():
        return HttpResponseForbidden("Not allowed")

    li = get_object_or_404(OrderItem, pk=lineitem_id, order=order)
    art = li.artwork

    url = art.get_download_url()
    if url:
        return redirect(force_download(url))

    messages.error(request, "The requested artwork is not available for download.")
    return redirect("library")

def force_download(url: str) -> str:
    if url and "res.cloudinary.com" in url and "/upload/" in url:
        return url.replace("/upload/", "/upload/fl_attachment/")
    return url
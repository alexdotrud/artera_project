from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db import transaction
from django.db.models import Prefetch, Count
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.http import HttpResponseBadRequest
import cloudinary.uploader
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator


from checkout.models import OrderItem, Order
from .forms import ProfileForm
from .models import Profile
from services.models import ArtworkRequest


@login_required
def profile(request):
    """Display and update user profile."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        new_email = (request.POST.get("email") or "").strip()
        new_username = (request.POST.get("username") or "").strip()

        if form.is_valid():
            # Handle username change
            if new_username and new_username != request.user.username:
                validator = UnicodeUsernameValidator()
                try:
                    validator(new_username)
                except ValidationError:
                    messages.error(
                        request,
                        "Invalid username."
                        "Use letters, numbers and @/./+/-/_ only."
                    )
                    return redirect("profile")
                if User.objects.filter(
                    username__iexact=new_username
                ).exclude(id=request.user.id).exists():
                    messages.error(request, "This username is already taken.")
                    return redirect("profile")
                
            with transaction.atomic():
                form.save()
                if new_username and new_username != request.user.username:
                    request.user.username = new_username
                    request.user.save(update_fields=["username"])
                if (
                    new_email
                    and new_email.lower()
                    != (request.user.email or "").lower()
                ):
                    # Create or reuse EmailAddress for the new email
                    ea = EmailAddress.objects.filter(
                        user=request.user,
                        email__iexact=new_email
                    ).first()
                    if not ea:
                        ea = EmailAddress(
                            user=request.user,
                            email=new_email,
                            primary=False,
                            verified=False
                        )
                        ea.save()

                    # Send confirmation to the new email
                    ea.send_confirmation(request)
                    messages.info(
                        request,
                        "We sent a verification link to your new email."
                    )
                else:
                    messages.success(request, "Profile updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "profiles/profile.html",
        {
            "form": form,
            "user_obj": request.user,
        },
    )


@login_required
def avatar_upload(request):
    """Upload or change avatar image."""
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    f = request.FILES.get("avatar")
    if not f:
        return HttpResponseBadRequest("No file")

    # CloudinaryField will upload on save
    profile.avatar = f
    profile.save(update_fields=["avatar"])
    messages.success(request, "Avatar updated.")
    return redirect("profile")


@login_required
def avatar_remove(request):
    if request.method != "POST":
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
        profile.save(update_fields=["avatar"])

    messages.success(request, "Avatar removed.")
    return redirect("profile")


@login_required
def library(request):
    """All orders history."""
    email = (request.user.email or "").strip()
    if not email:
        return render(request, "profiles/library.html", {"orders": []})

    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-date", "-id")
        .annotate(item_count=Count("lineitems"))
        .prefetch_related(
            Prefetch(
                "lineitems",
                queryset=OrderItem.objects.select_related("artwork")
                .order_by("id"),
            )
        )
    )

    requests_qs = (
        ArtworkRequest.objects.filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "profiles/library.html",
        {
            "orders": orders,
            "requests": requests_qs,
        },
    )


@login_required
def download_artwork(request, order_number, lineitem_id):
    """Download digital artwork file for an order line item."""
    # Order must belong to the logged-in user (by email)
    order = get_object_or_404(Order, order_number=order_number)
    if (
        not request.user.email
        or order.email.lower() != request.user.email.lower()
    ):
        return HttpResponseForbidden("Not allowed")

    li = get_object_or_404(OrderItem, pk=lineitem_id, order=order)
    art = li.artwork

    url = art.get_download_url()
    if url:
        return redirect(force_download(url))

    messages.error(
        request,
        "The requested artwork is not available for download."
    )
    return redirect("library")


def force_download(url: str) -> str:
    """Modify Cloudinary URL to force download."""
    if url and "res.cloudinary.com" in url and "/upload/" in url:
        return url.replace("/upload/", "/upload/fl_attachment/")
    return url

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Artwork
from services.models import ArtworkRequest, Offer
from .forms import ArtworkForm

@staff_member_required
def dashboard(request):
    artworks = Artwork.objects.order_by("-id")
    requests = ArtworkRequest.objects.order_by("-created_at")[:20]
    offers   = Offer.objects.order_by("-created_at")[:20]
    return render(request, "dashboard/dashboard.html", {
        "artworks": artworks,
        "requests": requests,
        "offers": offers,
        "artwork_form": ArtworkForm(),
    })

@staff_member_required
@require_POST
def artwork_create(request):
    form = ArtworkForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Artwork created.")
    else:
        messages.error(request, "Please fix the errors and try again.")
    return redirect("dashboard:dashboar")

@staff_member_required
def artwork_edit(request, pk):
    art = get_object_or_404(Artwork, pk=pk)
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Artwork updated.")
            return redirect("dashboard:dashboard")
        messages.error(request, "Please fix the errors and try again.")
    else:
        form = ArtworkForm(instance=art)
    return render(request, "dashboard/artwork_form.html", {"form": form, "art": art})

@staff_member_required
@require_POST
def artwork_delete(request, pk):
    get_object_or_404(Artwork, pk=pk).delete()
    messages.success(request, "Artwork deleted.")
    return redirect("dashboard:dashboard")

@staff_member_required
@require_POST
def request_update_status(request, pk):
    obj = get_object_or_404(ArtworkRequest, pk=pk)
    status = request.POST.get("status")
    if status in {"new", "in_progress", "accepted", "rejected"}:
        obj.status = status
        obj.save(update_fields=["status"])
        messages.success(request, f"Request #{obj.pk} → {obj.status}")
    else:
        messages.error(request, "Invalid status.")
    return redirect("dashboard:dashboard")

@staff_member_required
@require_POST
def request_delete(request, pk):
    get_object_or_404(ArtworkRequest, pk=pk).delete()
    messages.success(request, f"Request #{pk} deleted.")
    return redirect("dashboard:dashboard")
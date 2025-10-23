from django.shortcuts import render, redirect
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
    return redirect("dashboard")


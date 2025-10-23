from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

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

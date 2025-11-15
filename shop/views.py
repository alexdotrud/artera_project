from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Random

from .models import Artwork, Category, SIZE_CHOICES, SIZE_SURCHARGE


def all_artworks(request, category_id=None):
    artworks = Artwork.objects.select_related("category").order_by(Random())
    categories = Category.objects.order_by("name")

    if category_id:
        artworks = artworks.filter(category_id=category_id)
    query = None
    current_categories = None

    if "category" in request.GET:
        names = [
            c.strip()
            for c in request.GET["category"].split(",") if c.strip()]
        artworks = artworks.filter(category__name__in=names)
        current_categories = Category.objects.filter(name__in=names)

    context = {
        "artworks": artworks,
        "search_term": query,
        "current_categories": current_categories,
        "SIZE_SURCHARGE": SIZE_SURCHARGE,
        "categories": categories,
    }
    return render(request, "shop/list.html", context)


def artwork_detail(request, artwork_id):
    """A view to show individual artwork details"""
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    categories = Category.objects.all().order_by("name")

    # Size options
    size_options = []
    for code, label in SIZE_CHOICES:
        price = (
            artwork.price + SIZE_SURCHARGE[code]
        ).quantize(Decimal("0.01"))
        size_options.append(
            {
                "code": code,  # 'S' | 'M' | 'L'
                "label": label,  # '640x959'
                "price": price,  # Decimal
            }
        )

    # Default selection
    default_code = "S" if dict(SIZE_CHOICES).get("S") else SIZE_CHOICES[0][0]
    default_price = next(
        opt["price"] for opt in size_options if opt["code"] == default_code
    )

    return render(
        request,
        "shop/detail.html",
        {
            "artwork": artwork,
            "size_options": size_options,
            "default_size": default_code,
            "default_price": default_price,
            "categories": categories,
        },
    )


def artwork_search(request):
    """A view to search for artworks based on a query string"""
    query = request.GET.get("q", "").strip()

    artworks = Artwork.objects.select_related("category").order_by(Random())
    categories = Category.objects.order_by("name")
    current_categories = None

    if query:
        artworks = artworks.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        "artworks": artworks,
        "search_term": query,
        "current_categories": current_categories,
        "SIZE_SURCHARGE": SIZE_SURCHARGE,
        "categories": categories,
    }
    return render(request, "shop/list.html", context)

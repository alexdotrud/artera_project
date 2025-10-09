from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from .models import Artwork, Category, SIZE_CHOICES, SIZE_SURCHARGE


def all_artworks(request):
    artworks = Artwork.objects.all().select_related("category")
  # Temporarily disabled age filter until migration is fixed
# three_years_ago = timezone.now() - timedelta(days=3 * 365)
# artworks = artworks.filter(created_at__gte=three_years_ago)

    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort")
    direction = request.GET.get("direction")
    category_param = request.GET.get("category")
    current_categories = None

    # Sorting
    if sort:
        sortkey = sort
        if sort == "name":
            artworks = artworks.annotate(lower_name=Lower("name"))
            sortkey = "lower_name"
        elif sort == "category":
            sortkey = "category__name"
        if direction == "desc":
            sortkey = f"-{sortkey}"
        artworks = artworks.order_by(sortkey)

    # Category filter
    if category_param:
        names = [c.strip() for c in category_param.split(",") if c.strip()]
        artworks = artworks.filter(category__name__in=names)
        current_categories = Category.objects.filter(name__in=names)

    # Search
    if "q" in request.GET and not query:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse("all_artworks")) 

    if query:
        artworks = artworks.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    current_sorting = f"{sort or ''}_{direction or ''}"

    context = {
        "artworks": artworks,
        "search_term": query,
        "current_categories": current_categories,
        "current_sorting": current_sorting,
    }
    return render(request, "shop/list.html", context)


def artwork_detail(request, artwork_id):
    """ A view to show individual artwork details """
    artwork = get_object_or_404(Artwork, pk=artwork_id)
#three_years_ago = timezone.now() - timedelta(days=3 * 365)
   # artwork = get_object_or_404(
   #     Artwork.objects.filter(created_at__gte=three_years_ago),
    #    pk=artwork_id
#)


    # Size options
    size_options = []
    for code, label in SIZE_CHOICES:
        price = (artwork.price + SIZE_SURCHARGE[code]).quantize(Decimal("0.01"))
        size_options.append({
            "code": code,       # 'S' | 'M' | 'L'
            "label": label,     # '640x959'
            "price": price,     # Decimal
        })

    # Default selection
    default_code = "S" if dict(SIZE_CHOICES).get("S") else SIZE_CHOICES[0][0]
    default_price = next(opt["price"] for opt in size_options if opt["code"] == default_code)

    return render(request, "shop/detail.html", {
        "artwork": artwork,
        "size_options": size_options,
        "default_size": default_code,
        "default_price": default_price,
    })
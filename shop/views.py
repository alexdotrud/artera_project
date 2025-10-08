from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Artwork, Category


def all_artworks(request):
    """Show all artworks with sorting, filtering, and search."""
    artworks = Artwork.objects.all()
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
        return redirect(reverse("shop:list"))  # adjust to your URL name

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
    """Show a single artwork by PK."""
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    return render(request, "shop/detail.html", {"artwork": artwork})

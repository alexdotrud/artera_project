from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from .models import Artwork, Category, SIZE_CHOICES, SIZE_SURCHARGE


def all_artworks(request):
  # Temporarily disabled age filter until migration is fixed
# three_years_ago = timezone.now() - timedelta(days=3 * 365)
# artworks = artworks.filter(created_at__gte=three_years_ago)

    artworks = Artwork.objects.all().select_related("category")

    query = None
    current_categories = None
    sort = None
    direction = None

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                artworks = artworks.annotate(lower_name=Lower('name'))
                sortkey = 'lower_name'
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            artworks = artworks.order_by(sortkey)

        if 'category' in request.GET:
            names = [c.strip() for c in request.GET['category'].split(',') if c.strip()]
            artworks = artworks.filter(category__name__in=names)
            current_categories = Category.objects.filter(name__in=names)

        # Search
        if 'q' in request.GET:
            query = request.GET['q'].strip()
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                # adjust if you don't namespace:
                return redirect(reverse('shop:all_artworks'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            artworks = artworks.filter(queries)
    
    current_sorting = f"{sort or ''}_{direction or ''}"

    context = {
        'artworks': artworks,
        'search_term': query,
        'current_categories': current_categories,
        'current_sorting': current_sorting,
        'SIZE_SURCHARGE': SIZE_SURCHARGE,
    }
    return render(request, 'shop/list.html', context)


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
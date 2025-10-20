from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Artwork


def bag_contents(request):
    """ Works with the simple bag structure from your views """

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        artwork = get_object_or_404(Artwork, pk=item_id)

        # If item has sizes
        if isinstance(item_data, dict):
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * artwork.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'artwork': artwork,
                    'size': size,
                })
    
    # Delivery (optional – if you’re not using, just ignore)
    if total < getattr(settings, 'FREE_DELIVERY_THRESHOLD', 0):
        delivery = total * Decimal(getattr(settings, 'STANDARD_DELIVERY_PERCENTAGE', 0) / 100)
        free_delivery_delta = getattr(settings, 'FREE_DELIVERY_THRESHOLD', 0) - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': getattr(settings, 'FREE_DELIVERY_THRESHOLD', 0),
        'grand_total': grand_total,
    }

    return context

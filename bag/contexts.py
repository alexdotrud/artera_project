from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Artwork


def bag_contents(request):
    """ Works with the simple bag structure from your views """
    bag_items = []
    total = Decimal("0")
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        artwork = get_object_or_404(Artwork, pk=item_id)
        unit_price = Decimal(getattr(artwork, 'price', 0) or 0)

        # If item has sizes
        if isinstance(item_data, dict) and 'sizes' in item_data and isinstance(item_data['sizes'], dict):
            for size, quantity in item_data['sizes'].items():
                qty = int(quantity) if quantity else 1
                line_total = unit_price * qty
                total += line_total
                product_count += qty
                bag_items.append({
                    'item_id': item_id,
                    'artwork': artwork,
                    'size': size,
                    'quantity': qty,
                    'price': unit_price,
                    'lineitem_total': line_total,
                })
    
    # Delivery
    delivery = Decimal('0.00')
    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Artwork, SIZE_SURCHARGE

def bag_contents(request):
    """
    Make the shopping bag available globally.
    Works for both sized and non-sized items.
    """
    bag_items = []
    total = Decimal("0.00")
    product_count = 0
    bag = request.session.get("bag", {})

    for item_id, item_data in bag.items():
        artwork = get_object_or_404(Artwork, pk=item_id)

        for size, qty in item_data.get("items_by_size", {}).items():
            unit_price = (artwork.price + SIZE_SURCHARGE[size]).quantize(Decimal("0.01"))
            line_total = unit_price * qty
            total += line_total
            product_count += qty
            bag_items.append({
                "item_id": item_id,
                "quantity": qty,
                "artwork": artwork,
                "size": size,
                "unit_price": unit_price,
                "line_total": line_total,
            })

    # Delivery settings (safe defaults)
    free_delivery_threshold = getattr(settings, "FREE_DELIVERY_THRESHOLD", Decimal("50.00"))
    standard_delivery_percent = getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", Decimal("10"))

    if total < free_delivery_threshold:
        delivery = total * (standard_delivery_percent / 100)
        free_delivery_delta = free_delivery_threshold - total
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = total + delivery

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": free_delivery_threshold,
        "grand_total": grand_total,
    }

    return context

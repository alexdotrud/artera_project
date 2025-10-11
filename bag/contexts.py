from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Artwork, SIZE_SURCHARGE

def bag_contents(request):
    """
    Make the shopping bag available globally.
    Works for both sized and non-sized items.
    """
    bag_items = []
    product_count = 0
    total = 0.0
    bag = request.session.get("bag", {})

    for item_id, data in bag.items():
        # Skip malformed entries
        if not isinstance(data, dict):
            continue
        items_by_size = data.get("items_by_size") or {}
        if not isinstance(items_by_size, dict):
            continue

        try:
            pk = int(item_id)
        except (TypeError, ValueError):
            continue
        artwork = get_object_or_404(Artwork, pk=pk)

        # Rows per size
        for size, qty in items_by_size.items():
            code = (size or "").strip().upper()
            if code not in SIZE_SURCHARGE:
                continue
            try:
                qty = int(qty)
            except (TypeError, ValueError):
                continue
            if qty <= 0:
                continue

            base_price = float(artwork.price)
            surcharge  = float(SIZE_SURCHARGE[code])
            unit_price = round(base_price + surcharge, 2)
            line_total = round(unit_price * qty, 2)

            total = round(total + line_total, 2)
            product_count += qty

            bag_items.append({
                "item_id": pk,
                "artwork": artwork,
                "size": code,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line_total,
            })

    # Delivery settings
    free_delivery_threshold = float(getattr(settings, "FREE_DELIVERY_THRESHOLD", 50.00))
    delivery_pct = float(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 10.0))

    if total < free_delivery_threshold:
        delivery = round(total * (delivery_pct / 100.0),2)
        free_delivery_delta = round(free_delivery_threshold - total, 2)
    else:
        delivery = 0.0
        free_delivery_delta = 0.0

    grand_total = round(total + delivery, 2)

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

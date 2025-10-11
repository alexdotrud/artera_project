from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages

from shop.models import Artwork

def view_bag(request):
    """Render the bag contents page."""
    return render(request, "bag/bag.html")

def require_size(request):
    size_raw = request.POST.get("product_size")
    if not size_raw or not str(size_raw).strip():
        return None
    return str(size_raw).strip().upper()

def add_to_bag(request, item_id):
    """
    Add a quantity of the specified artwork to the shopping bag.
    """
    artwork = get_object_or_404(Artwork, pk=item_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, min(quantity, 99))

    redirect_url = request.POST.get("redirect_url") or reverse("view_bag")
    size = require_size(request)
    bag = request.session.get("bag", {})
    key = str(item_id)

    if not size:
        messages.error(request, "Please select a size before adding to bag.")
        return reverse("bag:view_bag")

    if key in bag and "items_by_size" in bag[key]:
        if quantity > 0:
            bag[key]["items_by_size"][size] = quantity
            messages.success(
                request,
                f'Updated size {size} {artwork.name} quantity to {bag[key]["items_by_size"][size]}'
            )
        else:
            bag[key]["items_by_size"].pop(size, None)
            messages.success(request, f"Removed size {size} {artwork.name} from your bag")
            if not bag[key]["items_by_size"]:
                bag.pop(key, None)

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))

def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified line.
    If quantity <= 0, remove it.
    """
    artwork = get_object_or_404(Artwork, pk=item_id)

    quantity = int(request.POST.get("quantity"))
    size = request.POST.get("product_size")
    bag = request.session.get("bag", {})

    if size:
        # sized items
        if item_id in bag and "items_by_size" in bag[item_id]:
            if quantity > 0:
                bag[item_id]["items_by_size"][size] = quantity
                messages.success(
                    request,
                    f'Updated size {size.upper()} {artwork.name} quantity to {bag[item_id]["items_by_size"][size]}',
                )
            else:
                # remove this size
                try:
                    del bag[item_id]["items_by_size"][size]
                except KeyError:
                    pass
                if not bag[item_id]["items_by_size"]:
                    bag.pop(item_id, None)
                messages.success(request, f"Removed size {size.upper()} {artwork.name} from your bag")

        if item_id in bag:
            if quantity > 0:
                bag[item_id] = quantity
                messages.success(request, f"Updated {artwork.name} quantity to {bag[item_id]}")
            else:
                bag.pop(item_id, None)
                messages.success(request, f"Removed {artwork.name} from your bag")

    request.session["bag"] = bag
    return redirect(reverse("bag:view_bag"))

def remove_from_bag(request, item_id):
    """Remove the item (or specific size) from the bag."""
    artwork = get_object_or_404(Artwork, pk=item_id)

    try:
        size = request.POST.get("product_size")
        bag = request.session.get("bag", {})

        # remove just this size
        if item_id in bag and "items_by_size" in bag[item_id]:
            bag[item_id]["items_by_size"].pop(size, None)
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id, None)
        messages.success(request, f"Removed size {size.upper()} {artwork.name} from your bag")

        request.session["bag"] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
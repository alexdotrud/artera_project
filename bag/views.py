from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from shop.models import Artwork

def view_bag(request):
    """Render the bag contents page."""
    return render(request, "bag/bag.html")

def add_to_bag(request, item_id):
    """
    Add a quantity of the specified artwork to the shopping bag.
    """
    artwork = get_object_or_404(Artwork, pk=item_id)

    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url") or reverse("bag:view_bag")
    size = request.POST.get("artwork_size")
    bag = request.session.get("bag", {})

    if item_id in bag:
        # ensure structure exists
        if "items_by_size" not in bag[item_id]:
            bag[item_id] = {"items_by_size": {}}
        if size in bag[item_id]["items_by_size"]:
            bag[item_id]["items_by_size"][size] += quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {artwork.name} quantity to {bag[item_id]["items_by_size"][size]}',
            )
        else:
            bag[item_id]["items_by_size"][size] = quantity
            messages.success(request, f"Added size {size.upper()} {artwork.name} to your bag")
    else:
        bag[item_id] = {"items_by_size": {size: quantity}}
        messages.success(request, f"Added size {size.upper()} {artwork.name} to your bag")

    request.session["bag"] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified line.
    If quantity <= 0, remove it.
    """
    artwork = get_object_or_404(Artwork, pk=item_id)

    quantity = int(request.POST.get("quantity"))
    size = request.POST.get("artwork_size")
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
        size = request.POST.get("artwork_size")
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
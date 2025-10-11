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

from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    get_object_or_404,
)
from django.contrib import messages
from django.views.decorators.http import require_POST
from shop.models import Artwork


def view_bag(request):
    """Render the bag contents page"""
    return render(request, "bag/bag.html")


@require_POST
def add_to_bag(request, item_id):
    """
    Add the specified artwork to the shopping bag.
    Shape enforced to match context:
      bag[item_id] = {"sizes": {size_code: 1, ...}}
    Quantities are fixed at 1 (no increments).
    """
    artwork = get_object_or_404(Artwork, pk=item_id)
    redirect_url = request.POST.get("redirect_url") or reverse("view_bag")

    size = request.POST.get("product_size")
    if not size:
        messages.error(request, "Please choose a size.")
        return redirect(redirect_url)

    bag = request.session.get("bag", {})
    key = str(item_id)

    entry = bag.get(key)
    if entry is None or not isinstance(entry, dict) or "sizes" not in entry:
        entry = {"sizes": {}}

    if size in entry["sizes"]:
        messages.info(
            request, f"{artwork.name} ({size.upper()}) is already in your bag."
        )
    else:
        entry["sizes"][size] = 1
        messages.success(
            request, f"Added {artwork.name} ({size.upper()}) to your bag."
        )

    bag[key] = entry
    request.session["bag"] = bag
    return redirect(redirect_url)


@require_POST
def remove_from_bag(request, item_id):
    """
    Remove the item (or a specific size) from the shopping bag.
    Works with shape: bag[item_id] = {"sizes": {...}}
    """
    artwork = get_object_or_404(Artwork, pk=item_id)
    size = request.POST.get("product_size")

    bag = request.session.get("bag", {})
    key = str(item_id)

    if (
        key not in bag
        or not isinstance(bag[key], dict)
        or "sizes" not in bag[key]
    ):
        messages.error(request, "Item not found in your bag.")
        return redirect(request.POST.get("next") or reverse("view_bag"))

    if size:
        if size in bag[key]["sizes"]:
            del bag[key]["sizes"][size]
            if not bag[key]["sizes"]:
                bag.pop(key, None)
            messages.success(
                request,
                f"Removed {artwork.name} ({size.upper()}) from your bag.",
            )
        else:
            messages.error(request, "That size is not in your bag.")
    else:
        bag.pop(key, None)
        messages.success(request, f"Removed {artwork.name} from your bag.")

    request.session["bag"] = bag
    return redirect(request.POST.get("next") or reverse("view_bag"))

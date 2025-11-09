from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from shop.models import Artwork

def view_bag(request):
    """ Render the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add the specified artwork to the bag without quantities.
    - If a size is provided, store each size at most once.
    - If item/size already exists, do nothing (idempotent).
    """
    artwork = get_object_or_404(Artwork, pk=item_id)

    redirect_url = request.POST.get('redirect_url') or reverse('view_bag')
    size = request.POST.get('product_size')
    bag = request.session.get('bag', {})
    key = str(item_id)

    if size:
        entry = bag.get(key)
        if entry is None:
            # start with a sizes list
            bag[key] = {'sizes': [size]}
            messages.success(request, f'Added {artwork.name} ({size.upper()}) to your bag.')
        else:
            # normalize legacy shapes
            if not isinstance(entry, dict) or 'sizes' not in entry or not isinstance(entry['sizes'], list):
                entry = {'sizes': []}
            if size in entry['sizes']:
                messages.info(request, f'{artwork.name} ({size.upper()}) is already in your bag.')
            else:
                entry['sizes'].append(size)
                bag[key] = entry
                messages.success(request, f'Added {artwork.name} ({size.upper()}) to your bag.')
    else:
        if key in bag:
            messages.info(request, f'{artwork.name} is already in your bag.')
        else:
            bag[key] = True
            messages.success(request, f'Added {artwork.name} to your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)

from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from shop.models import Artwork

def remove_from_bag(request, item_id):
    """Remove the item (or a specific size) from the bag (no quantities)."""
    artwork = get_object_or_404(Artwork, pk=item_id)
    bag = request.session.get('bag', {})
    key = str(item_id)
    size = request.POST.get('product_size')

    try:
        if key not in bag:
            messages.error(request, 'Item not found in your bag.')
            return HttpResponse(status=404)

        entry = bag[key]

        if size:
            if isinstance(entry, dict) and 'sizes' in entry and size in entry['sizes']:
                entry['sizes'].remove(size)
                if not entry['sizes']:
                    bag.pop(key, None)
                else:
                    bag[key] = entry
                messages.success(request, f'Removed {artwork.name} ({size.upper()}) from your bag')
            else:
                messages.error(request, 'Item/size not found in your bag.')
                return HttpResponse(status=404)
        else:
            # No size -> remove whole item (works for True or dict shapes)
            bag.pop(key, None)
            messages.success(request, f'Removed {artwork.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

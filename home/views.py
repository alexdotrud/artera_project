from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from shop.models import Artwork
from shop.models import SIZE_SURCHARGE


def homepege(request):
    return render(request, 'home/home.html')

def artwork_search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect("/")
    else:
        return render(request, "shop/list.html")
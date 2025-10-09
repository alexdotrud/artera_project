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

    # Split into words for multi-word search
    words = [word.strip() for word in q.split() if word.strip()]
    if not words:
        messages.error(request, "Invalid search query!")
        return redirect("/")
    
    q_objects = Q()
    for word in words:
        word_q = Q(name__icontains=word) | Q(description__icontains=word)
        q_objects &= word_q

    results = Artwork.objects.filter(q_objects).distinct().order_by('-created_at')

    return render(request, "home/search_results.html", {
        "q": q,
        "results": results,
        "SIZE_SURCHARGE": SIZE_SURCHARGE,
    })
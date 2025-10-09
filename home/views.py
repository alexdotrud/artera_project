from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import SearchDocument

def homepege(request):
    return render(request, 'home/home.html')

def search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect("/")

    results = SearchDocument.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(content__icontains=q) |
        Q(categories__name__icontains=q) |
        Q(categories__friendly_name__icontains=q)
).distinct()

    return render(request, "home/search_results.html", {
        "q": q,
        "results": results,
    })
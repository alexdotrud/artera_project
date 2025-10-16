from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages


def homepege(request):
    return render(request, 'home/home.html')

def artwork_search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('all_artworks'))

    params = {'q': q}
    if 'category' in request.GET:
        params['category'] = request.GET['category']

    return redirect(f"{reverse('all_artworks')}?{urlencode(params)}")
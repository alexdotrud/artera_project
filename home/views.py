from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber


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

@require_POST
def newsletter_subscribe(request):
    email = (request.POST.get("email") or "").strip().lower()

    if not email:
        messages.error(request, "Please enter a valid email.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    if NewsletterSubscriber.objects.filter(email=email).exists():
        messages.info(request, "This email is already subscribed.")
        return redirect(request.META.get("HTTP_REFERER", "home"))

    NewsletterSubscriber.objects.create(email=email)
    messages.success(request, "You've been subscribed to Artera updates!")
    return redirect(request.META.get("HTTP_REFERER", "home"))
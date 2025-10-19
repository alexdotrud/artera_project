from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArtworkRequestForm, OfferForm
from .models import ArtworkRequest

@login_required
def artwork_request(request):
    if request.method == "POST":
        form = ArtworkRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Request submitted for review.")
            return redirect("request_detail", pk=obj.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = ArtworkRequestForm()

    return render(request, "services/request_form.html", {"form": form})

@login_required
def request_detail(request, pk):
    obj = get_object_or_404(ArtworkRequest, pk=pk, user=request.user)
    return render(request, "services/request_detail.html", {"request_obj": obj})

def offer_request(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your offer was submitted.")
            return redirect("offer_success")
        messages.error(request, "Please fix the errors below.")
    else:
        form = OfferForm()
    return render(request, "services/offer_form.html", {"form": form})

def offer_success(request):
    return render(request, "services/offer_success.html")
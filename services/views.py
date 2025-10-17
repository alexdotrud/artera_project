from django.shortcuts import render

def artwork_request(request):
    return render(request, 'home/home.html')

def offer_request(request):
    return render(request, 'home/home.html')
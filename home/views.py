from django.shortcuts import render

def homepege(request):
    return render(request, 'home/home.html')
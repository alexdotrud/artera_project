from django.urls import path
from . import views

urlpatterns = [
    path('request', views.artwork_request, name='request'),
    path('offer', views.offer_request, name='offer'),
]
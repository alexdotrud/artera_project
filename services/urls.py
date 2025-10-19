from django.urls import path
from . import views

urlpatterns = [
    path('request', views.artwork_request, name='request'),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),
    path('offer', views.offer_request, name='offer'),
    path("offers/success/", views.offer_success, name="offer_success"),
]
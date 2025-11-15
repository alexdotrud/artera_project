from django.urls import path
from . import views


urlpatterns = [
    path('request', views.artwork_request, name='request'),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),
    path("requests/<int:pk>/edit/", views.request_edit, name="request_edit"),
    path(
        "requests/<int:pk>/delete/",
        views.request_delete,
        name="request_delete"
    ),
    path('offer', views.offer_request, name='offer'),
    path(
        "offer/success/<int:offer_id>/",
        views.offer_success,
        name="offer_success"
    ),
]

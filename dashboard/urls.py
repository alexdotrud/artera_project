from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard_operations, name="operations"),

    # Artworks actions
    path("artworks/new/", views.artwork_create, name="artwork_create"),
    path("artworks/<int:pk>/edit/", views.artwork_edit, name="artwork_edit"),
    path("artworks/<int:pk>/delete/", views.artwork_delete, name="artwork_delete"),

    # Requests actions
    path("requests/<int:pk>/status/", views.request_update_status, name="request_update_status"),
    path("requests/<int:pk>/delete/", views.request_delete, name="request_delete"),

    # Offers details (modal/page)
    path("offers/<int:pk>/", views.offer_detail, name="offer_detail"),
    path("offers/<int:pk>/delete/", views.offer_delete, name="offer_delete"),
]
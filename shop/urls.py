from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_artworks, name='shop'),
    path("<int:artwork_id>/", views.artwork_detail, name="detail"),
]
from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_artworks, name='all_artworks'),
    path(
        "category/<int:category_id>/",
        views.all_artworks,
        name="by_category"
        ),
    path("<int:artwork_id>/", views.artwork_detail, name="detail"),
    path("search/", views.artwork_search, name="artwork_search"),
]

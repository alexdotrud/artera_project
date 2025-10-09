from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepege, name='home'),
    path("search/", views.search, name="search"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name='profile'),
    path('library/', views.library, name='library')
]
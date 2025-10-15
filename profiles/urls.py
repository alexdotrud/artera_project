from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('library/', views.library, name='library')
]
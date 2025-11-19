from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepege, name='home'),
    path('artwork-search/', views.artwork_search, name='artwork_search'),
    path("newsletter/subscribe/",
        views.newsletter_subscribe,
        name="newsletter_subscribe"
    ),
]

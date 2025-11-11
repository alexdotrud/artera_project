from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile/avatar/upload/', views.avatar_upload, name='avatar_upload'),
    path('profile/avatar/remove/', views.avatar_remove, name='avatar_remove'),
    path('library/', views.library, name='library'),
    path( "library/download/<slug:order_number>/<int:lineitem_id>/",
    views.download_artwork, name="download_artwork"),
]
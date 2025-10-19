from django.contrib import admin
from .models import ArtworkRequest, Offer

@admin.register(ArtworkRequest)
class ArtworkRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "user__username")
    list_editable = ("status",)
    actions = ["mark_in_review", "mark_accepted", "mark_rejected"]

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "full_name", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "full_name", "email", "description")
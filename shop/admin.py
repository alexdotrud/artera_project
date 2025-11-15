from django.contrib import admin
from .models import Artwork, Category


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sku", "price",)
    list_filter = ("category",)
    search_fields = ("name", "sku", "description")
    autocomplete_fields = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    search_fields = ("name", "friendly_name")


@admin.display(description="Sizes")
def sizes(self, obj):
    return "S, M, L"

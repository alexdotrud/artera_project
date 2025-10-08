from django.contrib import admin
from .models import Artwork, Category

# Register your models here.

class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sku", "price", "has_sizes")
    list_filter = ("category", "has_sizes")
    search_fields = ("name", "sku", "description")
    autocomplete_fields = ("category",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    search_fields = ("name", "friendly_name")

admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Category, CategoryAdmin)
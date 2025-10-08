from django.contrib import admin
from .models import Artwork, Category

# Register your models here.

class ArtworkAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Category, CategoryAdmin)
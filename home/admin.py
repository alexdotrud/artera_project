from django.contrib import admin
from .models import SearchDocument


@admin.register(SearchDocument)
class SearchDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = (
        "title",
        "description",
        "content",
        "extra_text",
        "url",
        "categories__name",
        "categories__friendly_name"
    )
    filter_horizontal = ("categories",)

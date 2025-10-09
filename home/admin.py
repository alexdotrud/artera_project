from django.contrib import admin
from .models import SearchDocument

@admin.register(SearchDocument)
class SearchDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    search_fields = ("title", "description", "content", "url")
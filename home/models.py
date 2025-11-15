from django.db import models
from shop.models import Category


class SearchDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    extra_text = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=500)
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="search_docs"
    )

    def __str__(self):
        return self.title

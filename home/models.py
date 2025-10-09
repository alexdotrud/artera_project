from django.db import models
from shop.models import Category

# Create your models here.

class SearchDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    extra_text = models.TextField(blank=True, null=True) 
    url = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="search_docs")

    def __str__(self):
        return self.title
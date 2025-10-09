from django.db import models

# Create your models here.

class SearchDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.title
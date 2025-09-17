from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='books_added'
    )

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

from django.db import models

# Create your models here.
# AUTHOR model: stores the author's name.
# This is a simple model used as the "one" side of a one-to-many relationship with Book.
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# BOOK model: represents a single book.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
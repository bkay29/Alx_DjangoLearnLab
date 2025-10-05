                                                                                                                              # blog/models.py
from django.db import models 
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # <-- uses imported User

    # New: many-to-many relationship to Tag (optional; can be empty)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # keep this short and safe if post or author not yet saved
        return f'Comment by {self.author} on "{self.post}"'


class Tag(models.Model):
    """
    Simple Tag model. Name is unique (case-sensitive by DB) and slug is auto-generated.
    We keep slug so you can later use nicer URLs (e.g. /tags/<slug>/).
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # populate slug from name if not provided
        if not self.slug:
            # slugify lowercases and replaces spaces; keep it deterministic
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
                             
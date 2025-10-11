from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # users who follow this user
    # related_name='following' gives the reverse manager `some_user.following.all()`
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )

    def __str__(self):
        return self.username

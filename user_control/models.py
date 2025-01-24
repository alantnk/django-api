from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ("admin", "Admin"),
    ("basic", "Basic"),
    ("guest", "Guest"),
    ("guard", "Guard"),
)


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="basic")
    email = models.EmailField(unique=True)
    avatar = ResizedImageField(
        size=[300, 300], upload_to="users/avatars/%Y/%m/", blank=True, null=True
    )

    REQUIRED_FIELDS = ["email"]

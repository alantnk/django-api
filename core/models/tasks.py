from django.db import models
from django.conf import settings
from .base import BaseModel, STATUS_CHOICES


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    due_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="todo")
    closed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"Task - {self.title}"

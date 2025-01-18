from django.db import models
from .base import BaseModel
from .clients import Client
from .sales import Sale


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Task - {self.title}"

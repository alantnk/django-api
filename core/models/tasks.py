from django.db import models
from .base import BaseModel
from .clients import Client
from .sales import Sale


class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, on_delete=models.CASCADE, null=True
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=50, null=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"Task - {self.title}"

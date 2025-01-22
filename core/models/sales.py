from django.db import models
from django.conf import settings
from .base import BaseModel, STATUS_CHOICES
from .clients import Client


class Sale(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    chance = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES[1:], default="in_progress"
    )
    funnel_stage = models.CharField(max_length=150)
    expected_date = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sale - {self.client.office_name}"


class SaleHistory(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="history")
    changed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    field = models.CharField(max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()

    def __str__(self):
        return f"Sale {self.sale.id} History"

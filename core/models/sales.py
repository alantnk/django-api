from django.db import models
from .base import BaseModel
from .clients import Client


class Sale(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    chance = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=50)
    funnel_stage = models.CharField(max_length=50)
    expected_date = models.DateField()
    in_charge = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sale - {self.client.fantasy_name}"


class SaleHistory(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="history")
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    field = models.CharField(max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()

    def __str__(self):
        return f"Sale {self.sale.id} History"

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


STATUS_CHOICES = (
    ("todo", "A fazer"),
    ("in_progress", "Em andamento"),
    ("on_hold", "Em espera"),
    ("cancelled", "Cancelada"),
    ("pending", "Pendente"),
    ("done", "Concluida"),
)

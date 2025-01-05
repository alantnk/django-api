from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Client


@receiver(pre_save, sender=Client)
def set_uppercase(sender, instance, **kwargs):
    instance.fantasy_name = instance.fantasy_name.upper()
    instance.office_name = instance.office_name.upper()

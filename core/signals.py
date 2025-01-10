import os
import time
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from core.models import Client


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_save, sender=Client)
def set_uppercase(sender, instance, **kwargs):
    instance.fantasy_name = instance.fantasy_name.upper()
    instance.office_name = instance.office_name.upper()


@receiver(pre_delete, sender=Client)
def client_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Client.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Client)
def client_cover_update(sender, instance, *args, **kwargs):
    old_instance = Client.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    delete_cover(old_instance)

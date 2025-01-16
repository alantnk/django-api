import os
import time
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from core.models import Client, Sale, SaleHistory


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


@receiver(pre_save, sender=Sale)
def track_sale_changes(sender, instance, **kwargs):
    """
    Signal para rastrear alterações no model Sales e registrar no histórico.
    """
    # Verifica se a oportunidade já existe no banco
    if instance.pk:
        # Recupera a versão atual do objeto no banco de dados
        old_instance = Sale.objects.get(pk=instance.pk)

        # Itera pelos campos que devem ser monitorados
        fields_to_track = ["status", "estimated_value", "chance", "funnel_stage"]
        for field in fields_to_track:
            old_value = getattr(old_instance, field)
            new_value = getattr(instance, field)

            # Se o valor mudou, registra no histórico
            if old_value != new_value:

                print(old_value, new_value)
                print("MUDOU")
                SaleHistory.objects.create(
                    sale=instance,
                    in_charge=instance.user,
                    field=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                )

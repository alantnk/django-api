import os
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from core.models import Client, Sale, SaleHistory, Task, Tag, Category, Position


User = get_user_model()


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_save, sender=Tag)
@receiver(pre_save, sender=Category)
def set_name_uppercase(sender, instance, **kwargs):
    instance.name = instance.name.upper()


@receiver(pre_save, sender=Position)
def set_name_lowercase(sender, instance, **kwargs):
    instance.name = instance.name.lower()


@receiver(pre_save, sender=Client)
def set_client_names_uppercase(sender, instance, **kwargs):
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
@receiver(pre_save, sender=Task)
def set_closed(sender, instance, **kwargs):
    if instance.status in ["done", "cancelled"]:
        instance.closed = True


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

                SaleHistory.objects.create(
                    sale=instance,
                    user=instance.user,
                    field=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                )

import os
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

User = get_user_model()


def delete_avatar(instance):
    try:
        os.remove(instance.avatar.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=User)
def user_avatar_update(sender, instance, *args, **kwargs):
    old_instance = User.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    delete_avatar(old_instance)


@receiver(pre_save, sender=User)
def user_avatar_update(sender, instance, *args, **kwargs):
    old_instance = User.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    delete_avatar(old_instance)

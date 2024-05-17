from django.db.models.signals import post_save
from django.dispatch import receiver

from app_store.models import StoreModel
from app_user.models import UserModel

import uuid


@receiver(post_save, sender=StoreModel)
def set_store_top_users_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        users = UserModel.objects.filter(
            type__in=[
                UserModel.UserTypeOptions.Superuser,
                UserModel.UserTypeOptions.Staff,
            ]
        )
        for user in users:
            user.stores.add(instance)

from django.db.models.signals import post_save
from django.dispatch import receiver

from app_factor.models import FactorModel

import uuid


@receiver(post_save, sender=FactorModel)
def set_factor_tracking_code_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        if instance.tracking_code is None:
            instance.tracking_code = str(uuid.uuid4()).split("-")[-1]
            instance.save()

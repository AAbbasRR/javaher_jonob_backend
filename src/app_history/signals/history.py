from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
import json
import sys

from app_history.models import LogEntryModel


def get_serializable_dict(instance):
    """
    Return a dictionary representation of the instance, excluding non-serializable fields and sensitive fields.
    """
    data = instance.__dict__.copy()
    # Exclude the non-serializable _state field
    data.pop("_state", None)
    # Exclude sensitive fields
    sensitive_fields = ["password", "_password"]
    for field in sensitive_fields:
        data.pop(field, None)

    timestamp_fields = [
        "create_at",
        "updated_at",
        "deleted_at",
        "last_login",
        "date_joined",
    ]
    for field in timestamp_fields:
        if field in data and data[field] is not None:
            formatted_field = f"formatted_{field}"
            formatted_function = getattr(instance, formatted_field)
            data[field] = formatted_function()

    return data


@receiver(pre_save)
def log_pre_save(sender, instance, **kwargs):
    if (
        not issubclass(sender, LogEntryModel)
        and instance.pk
        and "migrate" not in sys.argv
    ):
        with transaction.atomic():
            try:
                old_instance = sender.objects.get(pk=instance.pk)
                data_before = json.loads(
                    json.dumps(
                        get_serializable_dict(old_instance), cls=DjangoJSONEncoder
                    )
                )
                instance._log_data_before = data_before
            except sender.DoesNotExist:
                pass


@receiver(post_save)
def log_post_save(sender, instance, created, **kwargs):
    if not issubclass(sender, LogEntryModel) and "migrate" not in sys.argv:
        with transaction.atomic():
            user = getattr(instance, "last_modified_by", None)
            data_after = json.loads(
                json.dumps(get_serializable_dict(instance), cls=DjangoJSONEncoder)
            )

            # Exclude _log_data_before from data_after
            data_after.pop("_log_data_before", None)

            action = "create" if created else "update"

            LogEntryModel.objects.create(
                model_name=sender.__name__,
                object_id=instance.pk,
                user=user,
                action=action,
                data_before=getattr(instance, "_log_data_before", None),
                data_after=data_after,
            )

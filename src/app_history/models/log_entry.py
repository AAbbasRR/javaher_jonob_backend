from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings
from app_user.models import UserModel


class LogEntry(models.Model):
    class ActionOptions(models.TextChoices):
        Create = "create", _("Create")
        Update = "update", _("Update")
        Delete = "delete", _("Delete")

    model_name = models.CharField(max_length=100, verbose_name=_("Model Name"))
    object_id = models.PositiveIntegerField(verbose_name=_("Object Id"))
    user = models.ForeignKey(
        UserModel,
        related_name="user_actions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("User"),
    )
    action = models.CharField(
        max_length=10,
        choices=ActionOptions.choices,
        default=ActionOptions.Update,
        verbose_name=_("Time"),
    )
    time = models.DateTimeField(auto_now_add=True, verbose_name=_("Time"))
    data_before = models.JSONField(null=True, blank=True, verbose_name=_("Data Before"))
    data_after = models.JSONField(null=True, blank=True, verbose_name=_("Data After"))

    def __str__(self):
        return f"{self.model_name} {self.action} by {self.user} at {self.time}"

    def formatted_time(self):
        return self.time.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

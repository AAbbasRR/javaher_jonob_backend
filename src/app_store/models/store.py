from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel


class Store(AbstractDateModel, AbstractSoftDeleteModel):
    name = models.CharField(max_length=32, verbose_name=_("Name"))

    def __str__(self):
        return f"{self.pk} {self.name}"

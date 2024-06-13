from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.db.models import AbstractDateModel
from utils.db import fields


class Driver(AbstractDateModel):
    mobile_number = fields.PhoneField(
        null=True, blank=True, verbose_name=_("Mobile Number")
    )
    full_name = models.CharField(max_length=124, verbose_name=_("Full Name"))
    plate_number = models.CharField(max_length=20, verbose_name=_("Plate Number"))

    def __str__(self):
        return f"{self.pk} {self.full_name} {self.mobile_number}"

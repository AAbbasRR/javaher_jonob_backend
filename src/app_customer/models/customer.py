from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.db.models import AbstractDateModel
from utils.db import fields


class CustomerManager(models.Manager):
    pass


class Customer(AbstractDateModel):
    mobile_number = fields.PhoneField(
        null=True, blank=True, verbose_name=_("Mobile Number")
    )
    full_name = models.CharField(max_length=124, verbose_name=_("Full Name"))
    customer_code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Customer Code"),
    )
    national_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name=_("National Code")
    )
    marketer = models.CharField(
        max_length=124, null=True, blank=True, verbose_name=_("Marketer")
    )

    objects = CustomerManager()

    def __str__(self):
        return f"{self.pk} {self.full_name} {self.mobile_number}"

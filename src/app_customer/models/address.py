from django.db import models
from django.utils.translation import gettext_lazy as _

from app_customer.models import CustomerModel

from utils.db.models import AbstractDateModel


class CustomerAddressManager(models.Manager):
    pass


class CustomerAddress(AbstractDateModel):
    customer = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name="customer_addresses",
        verbose_name=_("Customer"),
    )
    country = models.CharField(max_length=32, verbose_name=_("Country"))
    state = models.CharField(max_length=32, verbose_name=_("State"))
    full_address = models.TextField(verbose_name=_("Full Address"))

    objects = CustomerAddressManager()

    def __str__(self):
        return f"{self.pk} {self.customer.pk}"

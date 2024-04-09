from django.db import models
from django.utils.translation import gettext_lazy as _

from app_customer.models import CustomerModel, CustomerAddressModel
from app_store.models import StoreModel

from utils.db.models import AbstractDateModel


class FactorManager(models.Manager):
    pass


class Factor(AbstractDateModel):
    class PaymentTypeOptions(models.TextChoices):
        Check = "check", _("Check")
        Cash = "cash", _("Cash")
        Installment = "installment", _("Installment")

    tracking_code = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Tracking Code"),
    )
    customer = models.ForeignKey(
        CustomerModel,
        related_name="customer_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Customer"),
    )
    marketer = models.ForeignKey(
        CustomerModel,
        related_name="marketer_factors",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Marketer"),
    )
    address = models.ForeignKey(
        CustomerAddressModel,
        related_name="customer_address_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Address"),
    )
    is_accepted = models.BooleanField(default=False, verbose_name=_("Is Accepted"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    payment_type = models.CharField(
        max_length=11,
        choices=PaymentTypeOptions.choices,
        verbose_name=_("Payment Type"),
    )
    payment_status = models.BooleanField(
        default=False, verbose_name=_("Payment Status")
    )
    store = models.ForeignKey(
        StoreModel,
        related_name="store_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Store"),
    )

    objects = FactorManager()

    def __str__(self):
        return f"{self.pk} {self.tracking_code}"

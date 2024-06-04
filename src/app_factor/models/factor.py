from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from config import settings
from app_customer.models import CustomerModel, CustomerAddressModel
from app_store.models import StoreModel

from utils.db.models import AbstractDateModel
from utils.db import fields


class FactorManager(models.Manager):
    pass


class Factor(AbstractDateModel):
    class PermissionForAcceptOptions(models.TextChoices):
        Superuser = "superuser_staff", _("Superuser Or Staff")
        Secretary = "secretary_superuser_staff", _("Secretary Or Superuser Or Staff")

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
    address = models.ForeignKey(
        CustomerAddressModel,
        related_name="customer_address_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Address"),
    )
    factor_date = models.DateField(verbose_name=_("Factor Date"))
    discount_is_percent = models.BooleanField(
        default=False, verbose_name=_("Discount Is Percent")
    )
    discount_value = fields.PriceField(verbose_name=_("Discount Value"))
    is_accepted = models.BooleanField(default=True, verbose_name=_("Is Accepted"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    payment_status = models.BooleanField(
        default=False, verbose_name=_("Payment Status")
    )
    store = models.ForeignKey(
        StoreModel,
        related_name="store_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Store"),
    )
    permission_for_accept = models.CharField(
        max_length=25,
        choices=PermissionForAcceptOptions.choices,
        default=PermissionForAcceptOptions.Secretary,
        verbose_name=_("Permission For Accept"),
    )
    payment_amount = fields.PriceField(verbose_name=_("Payment Amount"))

    objects = FactorManager()

    def __str__(self):
        return f"{self.pk} {self.tracking_code}"

    def formatted_factor_date(self):
        return self.factor_date.strftime(settings.DATE_INPUT_FORMATS)

    def calculate_payment_amount(self):
        factor_items = self.factor_items.all()
        total = 0
        discount = self.discount_value
        for item in factor_items:
            total += (item.price + item.price * (item.tax / 100)) * item.count
        if self.discount_is_percent:
            discount = total * (self.discount_value / 100)
        self.payment_amount = total - discount
        self.save()


class FactorPaymentsManager(models.Manager):
    pass


class FactorPayments(AbstractDateModel):
    factor = models.ForeignKey(
        Factor,
        on_delete=models.CASCADE,
        related_name="factor_payments",
        verbose_name=_("Factor"),
    )
    amount = fields.PriceField(verbose_name=_("Amount"))

    objects = FactorPaymentsManager()

    def __str__(self):
        return f"{self.factor} {self.amount}"

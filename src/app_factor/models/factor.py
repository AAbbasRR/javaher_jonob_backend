from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile

from config import settings
from app_customer.models import CustomerModel, CustomerAddressModel
from app_store.models import StoreModel
from app_driver.models import DriverModel

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel
from utils.db import fields

from openpyxl import load_workbook
from io import BytesIO
import jdatetime


def factor_file_directory_path(instance, filename):
    return "factors/{0}/{1}".format(instance.id, filename)


class Factor(AbstractDateModel, AbstractSoftDeleteModel):
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
    driver = models.ForeignKey(
        DriverModel,
        null=True,
        blank=True,
        related_name="driver_factors",
        on_delete=models.CASCADE,
        verbose_name=_("Driver"),
    )
    factor_file = models.FileField(
        upload_to=factor_file_directory_path,
        null=True,
        blank=True,
        verbose_name=_("Factor File"),
    )

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

    def fill_factor_file(self):
        factor_template = load_workbook("factor.xlsx")
        cells = factor_template.active

        cells["J1"] = jdatetime.date.fromgregorian(date=self.factor_date).strftime(
            settings.DATE_INPUT_FORMATS
        )
        cells["J2"] = self.tracking_code
        cells["D4"] = self.customer.full_name
        cells["J4"] = self.customer.customer_code
        cells["D6"] = self.customer.national_code
        cells["J6"] = self.customer.mobile_number
        cells[
            "C8"
        ] = f"{self.address.country} - {self.address.state} - {self.address.city} - {self.address.street} - {self.address.full_address}"
        cells[
            "D29"
        ] = f"{self.driver.full_name} - {self.driver.mobile_number} - {self.driver.plate_number} - {self.driver.state}"
        cells["B33"] = self.description
        cells["J30"] = (
            self.payment_amount(self.discount_value / 100)
            if self.discount_is_percent
            else self.discount_value
        )
        for index, obj in enumerate(self.factor_items.all()):
            start_row = 12
            cells[f"B{start_row + index}"] = index + 1
            cells[
                f"C{start_row + index}"
            ] = f"{obj.product.name} - {obj.product.weight}Kg"
            cells[f"F{start_row + index}"] = obj.count
            cells[f"G{start_row + index}"] = obj.tax
            cells[f"H{start_row + index}"] = obj.price

        excel_file = BytesIO()
        factor_template.save(excel_file)
        excel_file.seek(0)

        self.factor_file.save("factor.xlsx", ContentFile(excel_file.read()), save=True)

    def factor_file_url(self, request):
        if not self.factor_file:
            return None

        protocol = (
            "https" if not settings.DEBUG and request.is_secure() else request.scheme
        )
        return f"{protocol}://{request.get_host()}{self.factor_file.url}"


class FactorPayments(AbstractDateModel, AbstractSoftDeleteModel):
    class PaymentTypeOptions(models.TextChoices):
        Check = "check", _("Check")
        Cash = "cash", _("Cash")
        Bank = "bank", _("Bank")

    factor = models.ForeignKey(
        Factor,
        on_delete=models.CASCADE,
        related_name="factor_payments",
        verbose_name=_("Factor"),
    )
    amount = fields.PriceField(verbose_name=_("Amount"))
    payment_type = models.CharField(
        max_length=11,
        choices=PaymentTypeOptions.choices,
        default=PaymentTypeOptions.Cash,
        verbose_name=_("Payment Type"),
    )
    payment_date = models.DateField(verbose_name=_("Payment Date"))
    tracking_code = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name=_("Tracking Code"),
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    def __str__(self):
        return f"{self.factor} {self.amount}"

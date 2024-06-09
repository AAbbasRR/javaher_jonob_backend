from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from app_product.models import ProductModel
from app_factor.models import FactorModel

from utils.db.models import AbstractDateModel
from utils.db import fields


class FactorItems(AbstractDateModel):
    factor = models.ForeignKey(
        FactorModel,
        related_name="factor_items",
        on_delete=models.CASCADE,
        verbose_name=_("Factor"),
    )
    product = models.ForeignKey(
        ProductModel,
        related_name="product_factors",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
    )
    price = fields.PriceField(null=True, blank=True, verbose_name=_("Price"))
    tax = fields.PercentField(null=True, blank=True, verbose_name=_("Tax"))
    count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("Count")
    )

    def __str__(self):
        return f"{self.pk} {self.factor} {self.product}"

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel
from utils.db import fields


class Product(AbstractDateModel, AbstractSoftDeleteModel):
    name = models.CharField(max_length=32, unique=True, verbose_name=_("Name"))
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Unit Of Measurement is Kg",
        verbose_name=_("Weight"),
    )
    price = fields.PriceField(verbose_name=_("Price"))
    tax = fields.PercentField(verbose_name=_("Tax"))

    def __str__(self):
        return f"{self.pk} {self.name} {self.weight}Kg"

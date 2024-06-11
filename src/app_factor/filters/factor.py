from django_filters import (
    FilterSet,
    DateTimeFromToRangeFilter,
)

from app_factor.models import FactorModel


class FactorListFilter(FilterSet):
    factor_date = DateTimeFromToRangeFilter(field_name="factor_date")

    class Meta:
        model = FactorModel
        fields = [
            "payment_status",
            "factor_date",
        ]

from django_filters import (
    FilterSet,
    DateTimeFromToRangeFilter,
)

from app_history.models import LogEntryModel


class LogEntryListFilter(FilterSet):
    time = DateTimeFromToRangeFilter(field_name="time")

    class Meta:
        model = LogEntryModel
        fields = [
            "model_name",
            "action",
            "time",
        ]

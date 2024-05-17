from django.db.models import Sum

from rest_framework import response

from app_factor.models import FactorModel, FactorItemsModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsStaffOrAbovePermission,
)

import pytz
from datetime import datetime, timedelta


class DashboardInfoDataAPIView(generics.CustomGenericAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsStaffOrAbovePermission,
    ]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        tehran_tz = pytz.timezone("Asia/Tehran")
        now = datetime.now(tehran_tz)
        start_of_today = tehran_tz.localize(datetime(now.year, now.month, now.day))
        start_of_tomorrow = start_of_today + timedelta(days=1)

        today_factors = FactorModel.objects.filter(
            is_accepted=True,
            create_at__gte=start_of_today,
            create_at__lt=start_of_tomorrow,
        )
        today_factor_ids = today_factors.values_list("id", flat=True)

        total_price = FactorItemsModel.objects.filter(
            factor_id__in=today_factor_ids
        ).aggregate(total_price=Sum("price"))["total_price"]
        if total_price is None:
            total_price = 0

        not_accepted_factors = FactorModel.objects.filter(is_accepted=False)

        return response.Response(
            {
                "factor_count": today_factors.count(),
                "factor_sell": total_price,
                "factor_not_accepted": not_accepted_factors.count(),
            }
        )

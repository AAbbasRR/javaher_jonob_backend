from rest_framework import response

from app_factor.models import FactorModel

from utils.views.versioning import BaseVersioning
from utils.views import generics
from utils.views.permissions import IsAuthenticatedPermission, IsStaffOrAbovePermission

import pytz
from datetime import datetime, timedelta


class marketerPieChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        tehran_tz = pytz.timezone("Asia/Tehran")
        now = datetime.now(tehran_tz)
        start_of_today = tehran_tz.localize(datetime(now.year, now.month, now.day))
        from_date = self.request.query_params.get("")

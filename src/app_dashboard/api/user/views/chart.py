from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth, TruncDay, TruncHour

from rest_framework import response

from app_factor.models import FactorModel, FactorItemsModel

from utils.views.versioning import BaseVersioning
from utils.views import generics
from utils.views.permissions import IsAuthenticatedPermission, IsStaffOrAbovePermission

import pytz
from datetime import datetime
from jdatetime import datetime as jdatetime


class MarketerPieChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        filter_time = from_date = self.request.query_params.get("filter", "monthly")
        iran_tz = pytz.timezone("Asia/Tehran")
        utc_tz = pytz.utc
        iran_now_time = datetime.now(iran_tz).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        utc_now_time = iran_now_time.astimezone(utc_tz)
        if filter_time == "daily":
            iran_start_date = datetime.now(iran_tz).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
        elif filter_time == "yearly":
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
        else:
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)

        queryset = (
            FactorModel.objects.filter(
                factor_date__range=[utc_start_date, utc_now_time], is_accepted=True
            )
            .values("customer__marketer")
            .annotate(count=Count("id"), total_payment_amount=Sum("payment_amount"))
            .order_by("customer__marketer")
        )

        return response.Response({"result": queryset})


class StoresPieChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        filter_time = from_date = self.request.query_params.get("filter", "monthly")
        iran_tz = pytz.timezone("Asia/Tehran")
        utc_tz = pytz.utc
        iran_now_time = datetime.now(iran_tz).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        utc_now_time = iran_now_time.astimezone(utc_tz)
        if filter_time == "daily":
            iran_start_date = datetime.now(iran_tz).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
        elif filter_time == "yearly":
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
        else:
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)

        queryset = (
            FactorModel.objects.filter(
                factor_date__range=[utc_start_date, utc_now_time], is_accepted=True
            )
            .values("store", "store__name")
            .annotate(count=Count("id"), total_payment_amount=Sum("payment_amount"))
            .order_by("store")
        )

        return response.Response({"result": queryset})


class SalesLineChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        filter_time = from_date = self.request.query_params.get("filter", "monthly")
        iran_tz = pytz.timezone("Asia/Tehran")
        utc_tz = pytz.utc
        iran_now_time = datetime.now(iran_tz).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        utc_now_time = iran_now_time.astimezone(utc_tz)
        if filter_time == "daily":
            iran_start_date = datetime.now(iran_tz).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorModel.objects.filter(
                    factor_date__range=[utc_start_date, utc_now_time], is_accepted=True
                )
                .annotate(date=TruncHour("create_at"))
                .values("date")
                .annotate(count=Count("id"), total_payment_amount=Sum("payment_amount"))
                .order_by("date")
            )
        elif filter_time == "yearly":
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorModel.objects.filter(
                    factor_date__range=[utc_start_date, utc_now_time], is_accepted=True
                )
                .annotate(date=TruncMonth("factor_date"))
                .values("date")
                .annotate(count=Count("id"), total_payment_amount=Sum("payment_amount"))
                .order_by("date")
            )
        else:
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorModel.objects.filter(
                    factor_date__range=[utc_start_date, utc_now_time], is_accepted=True
                )
                .annotate(date=TruncDay("factor_date"))
                .values("date")
                .annotate(count=Count("id"), total_payment_amount=Sum("payment_amount"))
                .order_by("date")
            )

        return response.Response({"result": queryset})


class ProductsBarChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        filter_time = from_date = self.request.query_params.get("filter", "monthly")
        iran_tz = pytz.timezone("Asia/Tehran")
        utc_tz = pytz.utc
        iran_now_time = datetime.now(iran_tz).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        utc_now_time = iran_now_time.astimezone(utc_tz)
        if filter_time == "daily":
            iran_start_date = datetime.now(iran_tz).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorItemsModel.objects.filter(
                    factor__factor_date__range=[utc_start_date, utc_now_time],
                    factor__is_accepted=True,
                )
                .values(
                    date=TruncHour("factor__create_at"), product_name=F("product__name")
                )
                .annotate(total_count=Sum("count"))
                .order_by("date", "product_name")
            )
        elif filter_time == "yearly":
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorItemsModel.objects.filter(
                    factor__factor_date__range=[utc_start_date, utc_now_time],
                    factor__is_accepted=True,
                )
                .values(
                    date=TruncMonth("factor__factor_date"),
                    product_name=F("product__name"),
                )
                .annotate(total_count=Sum("count"))
                .order_by("date", "product_name")
            )
        else:
            iran_start_date = (
                jdatetime.now(iran_tz)
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                .togregorian()
            )
            utc_start_date = iran_start_date.astimezone(utc_tz)
            queryset = (
                FactorItemsModel.objects.filter(
                    factor__factor_date__range=[utc_start_date, utc_now_time],
                    factor__is_accepted=True,
                )
                .values(
                    date=TruncDay("factor__factor_date"),
                    product_name=F("product__name"),
                )
                .annotate(total_count=Sum("count"))
                .order_by("date", "product_name")
            )

        results = []
        keys = set()
        current_date = None
        current_entry = None

        for item in queryset:
            date = item["date"]
            product = item["product_name"]
            total_count = item["total_count"]

            if date != current_date:
                if current_entry:
                    results.append(current_entry)
                current_date = date
                current_entry = {"date": date}

            current_entry[product] = total_count
            keys.add(product)

        if current_entry:
            results.append(current_entry)

        return response.Response({"keys": list(keys), "result": results})

from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDay

from rest_framework import response, exceptions

from app_factor.models import FactorModel, FactorItemsModel

from utils.views.versioning import BaseVersioning
from utils.views import generics
from utils.views.permissions import IsAuthenticatedPermission, IsStaffOrAbovePermission
from utils.exceptions.rest import ParameterRequiredException
from utils.base_errors import BaseErrors

from datetime import datetime


class MarketerPieChartAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsStaffOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        factor_date_after = self.request.query_params.get("factor_date_after", None)
        factor_date_before = self.request.query_params.get("factor_date_before", None)
        if factor_date_after is None or factor_date_before is None:
            raise ParameterRequiredException(
                ["factor_date_after", "factor_date_before"]
            )

        factor_date_after = datetime.strptime(factor_date_after, "%Y-%m-%d")
        factor_date_before = datetime.strptime(factor_date_before, "%Y-%m-%d")
        difference = (factor_date_after - factor_date_before).days

        if difference < -30:
            raise exceptions.ValidationError(
                {
                    "marketer_factor_date_after": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                    "marketer_factor_date_before": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                }
            )
        elif difference >= 0:
            raise exceptions.ValidationError(
                {
                    "marketer_factor_date_after": BaseErrors.invalid_field_value,
                    "marketer_factor_date_before": BaseErrors.invalid_field_value,
                }
            )

        queryset = (
            FactorModel.objects.filter(
                factor_date__range=[factor_date_after, factor_date_before],
                is_accepted=True,
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
        factor_date_after = self.request.query_params.get("factor_date_after", None)
        factor_date_before = self.request.query_params.get("factor_date_before", None)
        if factor_date_after is None or factor_date_before is None:
            raise ParameterRequiredException(
                ["factor_date_after", "factor_date_before"]
            )

        factor_date_after = datetime.strptime(factor_date_after, "%Y-%m-%d")
        factor_date_before = datetime.strptime(factor_date_before, "%Y-%m-%d")
        difference = (factor_date_after - factor_date_before).days

        if difference < -30:
            raise exceptions.ValidationError(
                {
                    "stores_factor_date_after": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                    "stores_factor_date_before": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                }
            )
        elif difference >= 0:
            raise exceptions.ValidationError(
                {
                    "stores_factor_date_after": BaseErrors.invalid_field_value,
                    "stores_factor_date_before": BaseErrors.invalid_field_value,
                }
            )

        queryset = (
            FactorModel.objects.filter(
                factor_date__range=[factor_date_after, factor_date_before],
                is_accepted=True,
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
        factor_date_after = self.request.query_params.get("factor_date_after", None)
        factor_date_before = self.request.query_params.get("factor_date_before", None)
        if factor_date_after is None or factor_date_before is None:
            raise ParameterRequiredException(
                ["factor_date_after", "factor_date_before"]
            )

        factor_date_after = datetime.strptime(factor_date_after, "%Y-%m-%d")
        factor_date_before = datetime.strptime(factor_date_before, "%Y-%m-%d")
        difference = (factor_date_after - factor_date_before).days

        if difference < -30:
            raise exceptions.ValidationError(
                {
                    "sales_factor_date_after": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                    "sales_factor_date_before": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                }
            )
        elif difference >= 0:
            raise exceptions.ValidationError(
                {
                    "sales_factor_date_after": BaseErrors.invalid_field_value,
                    "sales_factor_date_before": BaseErrors.invalid_field_value,
                }
            )

        queryset = (
            FactorModel.objects.filter(
                factor_date__range=[factor_date_after, factor_date_before],
                is_accepted=True,
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
        factor_date_after = self.request.query_params.get("factor_date_after", None)
        factor_date_before = self.request.query_params.get("factor_date_before", None)
        if factor_date_after is None or factor_date_before is None:
            raise ParameterRequiredException(
                ["factor_date_after", "factor_date_before"]
            )

        factor_date_after = datetime.strptime(factor_date_after, "%Y-%m-%d")
        factor_date_before = datetime.strptime(factor_date_before, "%Y-%m-%d")
        difference = (factor_date_after - factor_date_before).days

        if difference < -30:
            raise exceptions.ValidationError(
                {
                    "product_factor_date_after": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                    "product_factor_date_before": BaseErrors.filter_date_difference_should_not_more_than_30_days,
                }
            )
        elif difference >= 0:
            raise exceptions.ValidationError(
                {
                    "product_factor_date_after": BaseErrors.invalid_field_value,
                    "product_factor_date_before": BaseErrors.invalid_field_value,
                }
            )

        queryset = (
            FactorItemsModel.objects.filter(
                factor__factor_date__range=[factor_date_after, factor_date_before],
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

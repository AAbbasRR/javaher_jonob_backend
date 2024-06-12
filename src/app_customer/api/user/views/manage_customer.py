from django.http import HttpResponse

from rest_framework import response

from app_customer.api.user.serializers.manage_customer import (
    ListAddUpdateCustomerSerializer,
    ListCustomerExportResource,
)

from app_customer.models import CustomerModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSecretaryOrAbovePermission,
    IsWorkerOrAbovePermission,
)


class ListCreateCustomerAPIView(generics.CustomListCreateAPIView):
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all().order_by("customer_code")
    search_fields = [
        "mobile_number",
        "full_name",
        "customer_code",
        "national_code",
        "marketer",
        "customer_addresses__country",
        "customer_addresses__state",
        "customer_addresses__city",
        "customer_addresses__street",
        "customer_addresses__full_address",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedPermission(), IsWorkerOrAbovePermission()]
        return [IsAuthenticatedPermission(), IsSecretaryOrAbovePermission()]


class ExportListCustomerAPIView(generics.CustomListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsSecretaryOrAbovePermission]
    versioning_class = BaseVersioning
    queryset = CustomerModel.objects.all().order_by("customer_code")
    search_fields = [
        "mobile_number",
        "full_name",
        "customer_code",
        "national_code",
        "marketer",
        "customer_addresses__country",
        "customer_addresses__state",
        "customer_addresses__city",
        "customer_addresses__street",
        "customer_addresses__full_address",
    ]

    def get(self, *args, **kwargs):
        resource_class = ListCustomerExportResource()
        dataset = resource_class.export(self.filter_queryset(self.get_queryset()))

        result = HttpResponse(dataset.xlsx, content_type="text/xlsx")
        result["Content-Disposition"] = 'attachment; filename="export_customers.csv"'
        return result


class UpdateDeleteCustomerAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all()
    object_name = "Customer"


class LastCustomerCodeAPIView(generics.CustomGenericAPIView):
    permission_classes = [IsAuthenticatedPermission, IsSecretaryOrAbovePermission]
    versioning_class = BaseVersioning

    def get(self, request, *args, **kwargs):
        return response.Response(
            CustomerModel.objects.order_by("customer_code").last().customer_code + 1
        )

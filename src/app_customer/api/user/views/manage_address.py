from app_customer.api.user.serializers.manage_address import (
    ListAddUpdateCustomerAddressSerializer,
)

from app_customer.models import CustomerAddressModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSecretaryOrAbovePermission,
    IsWorkerOrAbovePermission,
)


class ListCreateCustomerAddressAPIView(generics.CustomListCreateAPIView):
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateCustomerAddressSerializer
    search_fields = [
        "country",
        "state",
        "city",
        "street",
        "full_address",
    ]

    def get_queryset(self):
        customer_value = self.request.query_params.get("customer", None)
        blank_addresses = CustomerAddressModel.objects.filter(customer=None)
        customer_addresses = CustomerAddressModel.objects.filter(
            customer=customer_value
        )
        return customer_addresses | blank_addresses

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedPermission(), IsWorkerOrAbovePermission()]
        return [IsAuthenticatedPermission(), IsSecretaryOrAbovePermission()]


class UpdateDeleteCustomerAddressAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateCustomerAddressSerializer
    queryset = CustomerAddressModel.objects.all()
    object_name = "Address"

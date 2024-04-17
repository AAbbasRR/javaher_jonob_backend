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
)


class ListCreateCustomerAddressAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateCustomerAddressSerializer
    queryset = CustomerAddressModel.objects.all()
    filterset_fields = ["customer"]
    search_fields = [
        "country",
        "state",
        "full_address",
    ]


class UpdateDeleteCustomerAddressAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateCustomerAddressSerializer
    queryset = CustomerAddressModel.objects.all()
    object_name = "Address"

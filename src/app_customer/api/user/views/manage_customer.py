from app_customer.api.user.serializers.manage_customer import (
    ListAddUpdateCustomerSerializer,
)

from app_customer.models import CustomerModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSecretaryOrAbovePermission,
)


class ListCreateCustomerAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all()
    search_fields = [
        "mobile_number",
        "full_name",
        "customer_code",
        "national_code",
    ]


class UpdateDeleteCustomerAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all()
    object_name = "Customer"

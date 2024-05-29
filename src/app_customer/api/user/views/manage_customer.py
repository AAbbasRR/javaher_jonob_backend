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
    IsWorkerOrAbovePermission,
)


class ListCreateCustomerAPIView(generics.CustomListCreateAPIView):
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all()
    search_fields = [
        "mobile_number",
        "full_name",
        "customer_code",
        "national_code",
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


class UpdateDeleteCustomerAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateCustomerSerializer
    queryset = CustomerModel.objects.all()
    object_name = "Customer"

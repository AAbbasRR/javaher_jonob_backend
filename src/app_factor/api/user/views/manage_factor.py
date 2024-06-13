from app_factor.api.user.serializers.manage_factor import (
    ListAddUpdateFactorSerializer,
    FactorPaymentsSerializer,
    AcceptFactorSerializer,
)

from app_factor.models import FactorModel, FactorPaymentsModel
from app_factor.filters.factor import FactorListFilter

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
    IsSecretaryOrAbovePermission,
    IsWorkerOrAbovePermission,
)


class ListCreateFactorAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsWorkerOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateFactorSerializer
    search_fields = [
        "tracking_code",
        "description",
        "customer__mobile_number",
        "customer__full_name",
        "customer__customer_code",
        "customer__national_code",
        "address__country",
        "address__state",
        "address__city",
        "address__street",
        "address__full_address",
        "store__name",
        "driver__full_name",
        "driver__mobile_number",
        "driver__plate_number",
    ]
    filterset_class = FactorListFilter

    def get_queryset(self):
        return FactorModel.objects.filter(store__in=self.request.user.stores.all())


class CreateFactorPaymentsAPIView(generics.CustomCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = FactorPaymentsSerializer


class UpdateDeleteFactorAPIView(generics.CustomUpdateDestroyAPIView):
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateFactorSerializer
    object_name = "Factor"

    def get_queryset(self):
        return FactorModel.objects.filter(store__in=self.request.user.stores.all())

    def get_permissions(self):
        if self.request.method == "PUT":
            return [IsAuthenticatedPermission(), IsSecretaryOrAbovePermission()]
        return [IsAuthenticatedPermission(), IsSuperUserPermission()]


class AcceptFactorAPIView(generics.CustomUpdateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AcceptFactorSerializer
    object_name = "Factor"

    def get_queryset(self):
        return FactorModel.objects.filter(store__in=self.request.user.stores.all())

from app_driver.api.user.serializers.manage_driver import (
    ListAddUpdateDriverSerializer,
)

from app_driver.models import DriverModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSecretaryOrAbovePermission,
    IsWorkerOrAbovePermission,
)


class ListCreateDriverAPIView(generics.CustomListCreateAPIView):
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateDriverSerializer
    queryset = DriverModel.objects.all()
    search_fields = ["mobile_number", "full_name", "plate_number", "state"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedPermission(), IsWorkerOrAbovePermission()]
        return [IsAuthenticatedPermission(), IsSecretaryOrAbovePermission()]


class UpdateDeleteDriverAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSecretaryOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateDriverSerializer
    queryset = DriverModel.objects.all()
    object_name = "Driver"

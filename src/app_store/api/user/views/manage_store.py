from app_store.api.user.serializers.manage_store import (
    ListAddUpdateStoreSerializer,
)

from app_store.models import StoreModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsStaffOrAbovePermission,
    IsWorkerOrAbovePermission,
)


class ListCreateStoreAPIView(generics.CustomListCreateAPIView):
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateStoreSerializer
    search_fields = [
        "name",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticatedPermission(), IsWorkerOrAbovePermission()]
        return [IsAuthenticatedPermission(), IsStaffOrAbovePermission()]

    def get_queryset(self):
        return self.request.user.stores.all()


class UpdateDeleteStoreAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsStaffOrAbovePermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateStoreSerializer
    queryset = StoreModel.objects.all()
    object_name = "Store"

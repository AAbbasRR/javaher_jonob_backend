from app_store.api.user.serializers.manage_store import (
    ListAddUpdateStoreSerializer,
)

from app_store.models import StoreModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
)


class ListCreateStoreAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateStoreSerializer
    queryset = StoreModel.objects.all()
    search_fields = [
        "name",
    ]


class UpdateDeleteStoreAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateStoreSerializer
    queryset = StoreModel.objects.all()
    object_name = "Store"

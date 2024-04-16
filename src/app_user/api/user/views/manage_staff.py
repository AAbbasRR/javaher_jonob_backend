from app_user.api.user.serializers.manage_staff import ListAddUpdateStaffSerializer

from app_user.models import UserModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
)


class ListCreateStaffAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateStaffSerializer
    search_fields = ["username", "first_name", "last_name"]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)


class UpdateDeleteStaffAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateStaffSerializer
    object_name = "Staff"

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

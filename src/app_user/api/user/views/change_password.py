from app_user.api.user.serializers.change_password import AdminChangePasswordSerializer

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission


class AdminChangePasswordAPIView(generics.CustomUpdateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

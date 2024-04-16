from app_user.api.user.serializers.change_password import ChangePasswordSerializer

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission


class ChangePasswordAPIView(generics.CustomUpdateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

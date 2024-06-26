from app_history.api.user.serializers.manage_history import (
    ListLogEntrySerializer,
)

from app_history.models import LogEntryModel
from app_history.filters.history import LogEntryListFilter

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
)


class ListLogEntryAPIView(generics.CustomListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsSuperUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListLogEntrySerializer
    queryset = LogEntryModel.objects.all().order_by("-id")
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
    filterset_class = LogEntryListFilter

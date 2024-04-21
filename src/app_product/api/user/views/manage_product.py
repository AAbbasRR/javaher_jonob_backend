from app_product.api.user.serializers.manage_product import (
    ListAddUpdateProductSerializer,
)

from app_product.models import ProductModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsSuperUserPermission,
)


class ListCreateProductAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ListAddUpdateProductSerializer
    queryset = ProductModel.objects.all()
    search_fields = ["name", "weight", "price"]


class UpdateDeleteProductAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = ListAddUpdateProductSerializer
    queryset = ProductModel.objects.all()
    object_name = "Product"

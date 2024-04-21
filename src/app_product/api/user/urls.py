from django.urls import path

from .views import *

app_name = "app_product_user"
urlpatterns = [
    # manage product
    path(
        "manage/list_create/",
        ListCreateProductAPIView.as_view(),
        name="list_create_manage_product",
    ),
    path(
        "manage/update_delete/",
        UpdateDeleteProductAPIView.as_view(),
        name="update_delete_manage_product",
    ),
]

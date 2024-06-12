from django.urls import path

from .views import *

app_name = "app_customer_user"
urlpatterns = [
    # customer
    path(
        "manage/list_create/",
        ListCreateCustomerAPIView.as_view(),
        name="manage_customer_list_create",
    ),
    path(
        "manage/export/",
        ExportListCustomerAPIView.as_view(),
        name="manage_export_customer",
    ),
    path(
        "manage/last_customer_code/",
        LastCustomerCodeAPIView.as_view(),
        name="manage_last_customer_cde",
    ),
    path(
        "manage/update_delete/",
        UpdateDeleteCustomerAPIView.as_view(),
        name="manage_customer_update_delete",
    ),
    # customer address
    path(
        "manage/address/list_create/",
        ListCreateCustomerAddressAPIView.as_view(),
        name="manage_customer_address_list_create",
    ),
    path(
        "manage/address/update_delete/",
        UpdateDeleteCustomerAddressAPIView.as_view(),
        name="manage_customer_address_update_delete",
    ),
]

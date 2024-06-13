from django.urls import path

from .views import *

app_name = "app_driver_user"
urlpatterns = [
    # driver
    path(
        "manage/list_create/",
        ListCreateDriverAPIView.as_view(),
        name="manage_driver_list_create",
    ),
    path(
        "manage/update_delete/",
        UpdateDeleteDriverAPIView.as_view(),
        name="manage_driver_update_delete",
    ),
]

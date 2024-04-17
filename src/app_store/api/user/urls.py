from django.urls import path

from .views import *

app_name = "app_store_user"
urlpatterns = [
    # store
    path(
        "manage/list_create/",
        ListCreateStoreAPIView.as_view(),
        name="manage_store_list_create",
    ),
    path(
        "manage/update_delete/",
        UpdateDeleteStoreAPIView.as_view(),
        name="manage_store_update_delete",
    ),
]

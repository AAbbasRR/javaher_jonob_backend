from django.urls import path

from .views import *

app_name = "app_factor_user"
urlpatterns = [
    # manage product
    path(
        "manage/list_create/",
        ListCreateFactorAPIView.as_view(),
        name="list_create_manage_factor",
    ),
    path(
        "manage/update_delete/",
        UpdateDeleteFactorAPIView.as_view(),
        name="update_delete_manage_factor",
    ),
    path(
        "manage/accept_factor/",
        AcceptFactorAPIView.as_view(),
        name="accept_factor",
    ),
]

from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

app_name = "app_user_user"
urlpatterns = [
    # login
    path("auth/login/", UserLoginAPIView.as_view(), name="login"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="login_token_refresh"),
    # info
    path("auth/info/", UserInfoAPIView.as_view(), name="info_account"),
    # change password
    path(
        "auth/change_password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    # manage staffs
    path(
        "manage/staff/list_create/",
        ListCreateStaffAPIView.as_view(),
        name="list_create_manage_staff",
    ),
    path(
        "manage/staff/update_delete/",
        UpdateDeleteStaffAPIView.as_view(),
        name="update_delete_manage_staff",
    ),
]

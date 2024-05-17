from django.urls import path

from .views import *

app_name = "app_dashboard_user"
urlpatterns = [
    # dashboard
    path(
        "info_data/",
        DashboardInfoDataAPIView.as_view(),
        name="info_data",
    ),
]

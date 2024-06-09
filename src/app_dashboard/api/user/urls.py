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
    path(
        "marketer_chart/",
        MarketerPieChartAPIView.as_view(),
        name="marketer_data",
    ),
    path(
        "stores_chart/",
        StoresPieChartAPIView.as_view(),
        name="stores_data",
    ),
    path(
        "sales_chart/",
        SalesLineChartAPIView.as_view(),
        name="sales_data",
    ),
    path(
        "products_chart/",
        ProductsBarChartAPIView.as_view(),
        name="products_data",
    ),
]

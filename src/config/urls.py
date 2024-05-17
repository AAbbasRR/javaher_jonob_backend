from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

v1_urlpatterns = [
    path("user/", include("app_user.api.user.urls", namespace="app_user_user")),
    path(
        "customer/",
        include("app_customer.api.user.urls", namespace="app_customer_user"),
    ),
    path(
        "store/",
        include("app_store.api.user.urls", namespace="app_store_user"),
    ),
    path(
        "product/",
        include("app_product.api.user.urls", namespace="app_product_user"),
    ),
    path(
        "factor/",
        include("app_factor.api.user.urls", namespace="app_factor_user"),
    ),
    path(
        "dashboard/",
        include("app_dashboard.api.user.urls", namespace="app_dashboard_user"),
    ),
]

urlpatterns = [
    path("api/<str:version>/", include(v1_urlpatterns)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = "utils.url_handlers.custom_404_response"
handler500 = "utils.url_handlers.custom_500_response"

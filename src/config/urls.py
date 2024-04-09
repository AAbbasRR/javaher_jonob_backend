from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    path,
    include,
)
from django.conf import settings
from django.conf.urls.static import static

v1_user_urlpatterns = []

v1_admin_urlpatterns = []

v1_urlpatterns = [
    path("user/", include(v1_user_urlpatterns)),
    path("admin/", include(v1_admin_urlpatterns)),
]

urlpatterns = [
    path("api/<str:version>/", include(v1_urlpatterns)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = "utils.url_handlers.custom_404_response"
handler500 = "utils.url_handlers.custom_500_response"

from django.urls import path

from .views import *

app_name = "app_history_user"
urlpatterns = [
    # log entry
    path(
        "manage/list/",
        ListLogEntryAPIView.as_view(),
        name="manage_history_list",
    ),
]

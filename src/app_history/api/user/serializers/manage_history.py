from rest_framework import serializers

from app_history.models import LogEntryModel
from app_user.models import UserModel

from utils.serializers.serializer import CustomModelSerializer


class UserSerializer(CustomModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "type_display",
        )


class ListLogEntrySerializer(CustomModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = LogEntryModel
        fields = (
            "id",
            "model_name",
            "object_id",
            "user",
            "action_display",
            "formatted_time",
            "data_before",
            "data_after",
        )

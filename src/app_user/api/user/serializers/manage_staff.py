from django.db import transaction

from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateStaffSerializer(CustomModelSerializer):
    type = serializers.CharField(source="get_type_display")

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "type",
            "formatted_last_login",
            "formatted_date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return UserModel.objects.register_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            if password is not None:
                instance.set_password(password)
            instance.save()
        return instance

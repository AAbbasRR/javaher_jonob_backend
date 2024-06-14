from django.db import transaction

from rest_framework import serializers

from app_user.models import UserModel
from app_store.models import StoreModel

from utils.serializers.serializer import CustomModelSerializer
from utils.db.validators import UniqueValidator


class ListAddUpdateStaffSerializer(CustomModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=UserModel.objects.all()),
        ],
    )

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
            "type_display",
            "stores",
            "formatted_last_login",
            "formatted_date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}, "stores": {"default": []}}

    def create(self, validated_data):
        stores_data = validated_data.pop("stores", None)
        user = UserModel.objects.register_user(**validated_data)
        if user.type in ["superuser", "staff"]:
            stores_data = StoreModel.objects.all()
        if stores_data:
            user.stores.set(stores_data)
        user.last_modified_by = self.user
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        stores_data = validated_data.pop("stores", None)
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            if password is not None:
                instance.set_password(password)
            if instance.type in ["superuser", "staff"]:
                stores_data = StoreModel.objects.all()
            if stores_data:
                instance.stores.set(stores_data)
            instance.last_modified_by = self.user
            instance.save()
        return instance

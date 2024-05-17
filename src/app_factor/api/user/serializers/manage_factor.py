from django.db import transaction

from rest_framework import serializers

from app_factor.models import FactorModel, FactorItemsModel
from app_customer.models import CustomerModel, CustomerAddressModel

from utils.serializers.serializer import CustomModelSerializer
from utils.exceptions.rest import UserDontHavePermissionException


class CustomerSerializer(CustomModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            "mobile_number",
            "full_name",
            "customer_code",
        )


class CustomerAddressSerializer(CustomModelSerializer):
    class Meta:
        model = CustomerAddressModel
        fields = (
            "country",
            "state",
            "full_address",
        )


class FactorItemsSerializer(CustomModelSerializer):
    class Meta:
        model = FactorItemsModel
        fields = (
            "id",
            "product",
            "price",
            "tax",
            "count",
        )


class ListAddUpdateFactorSerializer(CustomModelSerializer):
    payment_type_display = serializers.CharField(
        source="get_payment_type_display", read_only=True
    )
    factor_items = FactorItemsSerializer(required=True, many=True)
    store_data = serializers.SerializerMethodField()
    customer_data = serializers.SerializerMethodField()
    marketer_data = serializers.SerializerMethodField()
    address_data = serializers.SerializerMethodField()
    can_accept = serializers.SerializerMethodField()

    class Meta:
        model = FactorModel
        fields = (
            "id",
            "tracking_code",
            "customer",
            "marketer",
            "address",
            "customer_data",
            "marketer_data",
            "address_data",
            "is_accepted",
            "description",
            "payment_type",
            "payment_type_display",
            "payment_status",
            "store",
            "factor_items",
            "can_accept",
            "store_data",
            "formatted_create_at",
            "formatted_updated_at",
        )
        extra_kwargs = {
            "is_accepted": {"read_only": True},
        }

    def get_customer_data(self, obj):
        return CustomerSerializer(obj.customer, many=False).data

    def get_marketer_data(self, obj):
        return CustomerSerializer(obj.marketer, many=False).data

    def get_address_data(self, obj):
        return CustomerAddressSerializer(obj.address, many=False).data

    def get_store_data(self, obj):
        return obj.store.name

    def get_can_accept(self, obj):
        return self.user.type in obj.permission_for_accept

    def create(self, validated_data):
        product_items = validated_data.pop("factor_items", [])
        factor = FactorModel.objects.create(**validated_data)
        for product in product_items:
            FactorItemsModel.objects.create(factor=factor, **product)
        if self.user.type in [
            self.user.UserTypeOptions.Superuser,
            self.user.UserTypeOptions.Staff,
        ]:
            factor.is_accepted = True
        else:
            if self.user.type == self.user.UserTypeOptions.Worker:
                factor.permission_for_accept = (
                    FactorModel.PermissionForAcceptOptions.Secretary
                )
            else:
                factor.permission_for_accept = (
                    FactorModel.PermissionForAcceptOptions.Superuser
                )
        factor.save()
        return factor

    def update(self, instance, validated_data):
        product_items = validated_data.pop("factor_items", [])
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.save()
        instance.factor_items.all().delete()
        for product in product_items:
            FactorItemsModel.objects.create(factor=instance, **product)
        if self.user.type in [
            self.user.UserTypeOptions.Superuser,
            self.user.UserTypeOptions.Staff,
        ]:
            instance.is_accepted = True
        else:
            if self.user.type == self.user.UserTypeOptions.Worker:
                instance.permission_for_accept = (
                    FactorModel.PermissionForAcceptOptions.Secretary
                )
            else:
                instance.permission_for_accept = (
                    FactorModel.PermissionForAcceptOptions.Superuser
                )
        instance.save()
        return instance


class AcceptFactorSerializer(CustomModelSerializer):
    class Meta:
        model = FactorModel
        fields = (
            "id",
            "is_accepted",
        )
        extra_kwargs = {"is_accepted": {"read_only": True}}

    def update(self, instance, validated_data):
        if self.user.type in instance.permission_for_accept:
            instance.is_accepted = True
            instance.save()
            return instance
        else:
            raise UserDontHavePermissionException()

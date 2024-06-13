from django.db import transaction

from rest_framework import serializers

from app_factor.models import FactorModel, FactorItemsModel, FactorPaymentsModel
from app_customer.models import CustomerModel, CustomerAddressModel
from app_driver.models import DriverModel

from utils.serializers.serializer import CustomModelSerializer
from utils.exceptions.rest import (
    UserDontHavePermissionException,
    InvalidAmountException,
)


class CustomerSerializer(CustomModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            "mobile_number",
            "full_name",
            "customer_code",
            "marketer",
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
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = FactorItemsModel
        fields = (
            "id",
            "product",
            "name",
            "weight",
            "price",
            "tax",
            "count",
        )

    def get_id(self, obj):
        return obj.product.id

    def get_name(self, obj):
        return obj.product.name

    def get_weight(self, obj):
        return obj.product.weight


class FactorPaymentsSerializer(CustomModelSerializer):
    payment_type_display = serializers.CharField(
        source="get_payment_type_display", read_only=True
    )

    class Meta:
        model = FactorPaymentsModel
        fields = (
            "id",
            "factor",
            "amount",
            "formatted_create_at",
            "payment_type",
            "payment_date",
            "tracking_code",
            "description",
            "payment_type_display",
        )

    def validate(self, attrs):
        payments_history = attrs["factor"].factor_payments.all()
        total = 0
        for item in payments_history:
            total += item.amount
        if (attrs["factor"].payment_amount - total) < attrs["amount"]:
            raise InvalidAmountException(attrs["factor"].payment_amount - total)
        return attrs

    def create(self, validated_data):
        factor_payment = FactorPaymentsModel.objects.create(**validated_data)
        payments_history = factor_payment.factor.factor_payments.all()
        total = 0
        for item in payments_history:
            total += item.amount
        if (factor_payment.factor.payment_amount - total) == 0:
            factor_payment.factor.payment_status = True
            factor_payment.factor.save()
        return factor_payment


class DriverSerializer(CustomModelSerializer):
    class Meta:
        model = DriverModel
        fields = (
            "mobile_number",
            "full_name",
            "plate_number",
        )


class ListAddUpdateFactorSerializer(CustomModelSerializer):
    factor_items = FactorItemsSerializer(required=True, many=True)
    factor_payments = FactorPaymentsSerializer(many=True, read_only=True)
    store_data = serializers.SerializerMethodField()
    customer_data = serializers.SerializerMethodField()
    address_data = serializers.SerializerMethodField()
    can_accept = serializers.SerializerMethodField()
    driver_data = serializers.SerializerMethodField()

    class Meta:
        model = FactorModel
        fields = (
            "id",
            "tracking_code",
            "customer",
            "driver",
            "address",
            "customer_data",
            "address_data",
            "driver_data",
            "factor_date",
            "discount_is_percent",
            "discount_value",
            "is_accepted",
            "description",
            "payment_status",
            "payment_amount",
            "store",
            "factor_items",
            "factor_payments",
            "can_accept",
            "store_data",
            "formatted_create_at",
            "formatted_updated_at",
        )
        extra_kwargs = {
            "is_accepted": {"read_only": True},
            "payment_status": {"read_only": True},
        }

    def get_customer_data(self, obj):
        return CustomerSerializer(obj.customer, many=False).data

    def get_address_data(self, obj):
        return CustomerAddressSerializer(obj.address, many=False).data

    def get_driver_data(self, obj):
        return DriverSerializer(obj.driver, many=False).data

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
        factor.calculate_payment_amount()
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
        instance.calculate_payment_amount()
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

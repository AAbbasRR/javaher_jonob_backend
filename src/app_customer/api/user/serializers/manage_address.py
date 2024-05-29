from django.db import transaction

from app_customer.models import CustomerAddressModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateCustomerAddressSerializer(CustomModelSerializer):
    class Meta:
        model = CustomerAddressModel
        fields = (
            "id",
            "customer",
            "country",
            "state",
            "city",
            "street",
            "full_address",
            "formatted_create_at",
            "formatted_updated_at",
        )

    def create(self, validated_data):
        return CustomerAddressModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.save()
        return instance

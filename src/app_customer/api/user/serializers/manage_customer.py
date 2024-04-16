from django.db import transaction

from app_customer.models import CustomerModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateCustomerSerializer(CustomModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            "id",
            "mobile_number",
            "full_name",
            "customer_code",
            "national_code",
            "formatted_create_at",
            "formatted_updated_at",
        )

    def create(self, validated_data):
        return CustomerModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.save()
        return instance

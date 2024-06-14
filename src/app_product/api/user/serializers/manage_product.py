from django.db import transaction

from app_product.models import ProductModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateProductSerializer(CustomModelSerializer):
    class Meta:
        model = ProductModel
        fields = (
            "id",
            "name",
            "weight",
            "price",
            "tax",
            "formatted_create_at",
            "formatted_updated_at",
        )

    def create(self, validated_data):
        return ProductModel.objects.create(last_modified_by=self.user, **validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.last_modified_by = self.user
            instance.save()
        return instance

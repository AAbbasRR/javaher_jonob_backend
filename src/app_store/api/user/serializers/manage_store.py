from django.db import transaction

from app_store.models import StoreModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateStoreSerializer(CustomModelSerializer):
    class Meta:
        model = StoreModel
        fields = (
            "id",
            "name",
            "formatted_create_at",
            "formatted_updated_at",
        )

    def create(self, validated_data):
        return StoreModel.objects.create(last_modified_by=self.user, **validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.last_modified_by = self.user
            instance.save()
        return instance

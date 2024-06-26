from django.db import transaction

from app_driver.models import DriverModel

from utils.serializers.serializer import CustomModelSerializer


class ListAddUpdateDriverSerializer(CustomModelSerializer):
    class Meta:
        model = DriverModel
        fields = (
            "id",
            "mobile_number",
            "full_name",
            "plate_number",
            "state",
            "formatted_create_at",
            "formatted_updated_at",
        )

    def create(self, validated_data):
        return DriverModel.objects.create(last_modified_by=self.user, **validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            for field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
            instance.last_modified_by = self.user
            instance.save()
        return instance

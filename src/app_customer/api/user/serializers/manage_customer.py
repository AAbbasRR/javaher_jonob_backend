from django.db import transaction
from django.utils.translation import gettext_lazy as _

from import_export import resources, fields

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
            "marketer",
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


class ListCustomerExportResource(resources.ModelResource):
    customer_code = fields.Field(column_name=_("customer_code"))
    national_code = fields.Field(column_name=_("national_code"))
    mobile_number = fields.Field(column_name=_("mobile_number"))
    full_name = fields.Field(column_name=_("full_name"))
    marketer = fields.Field(column_name=_("marketer"))

    class Meta:
        model = CustomerModel
        fields = (
            "customer_code",
            "national_code",
            "mobile_number",
            "full_name",
            "marketer",
        )

    def dehydrate_national_code(self, obj):
        if obj.national_code is None:
            return ""
        else:
            return obj.national_code

    def dehydrate_mobile_number(self, obj):
        if obj.mobile_number is None:
            return ""
        else:
            return obj.mobile_number

    def dehydrate_marketer(self, obj):
        if obj.marketer is None:
            return ""
        else:
            return obj.marketer

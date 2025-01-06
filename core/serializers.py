from core.models import Client, Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class AddressSerializer(serializers.Serializer):
    location = serializers.CharField()
    state_code = serializers.CharField()
    zip_code = serializers.CharField()
    district = serializers.CharField()
    address = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            "id",
            "fantasy_name",
            "office_name",
            "category",
            "full_category",
            "idoc",
            "location",
            "state_code",
            "zip_code",
            "district",
            "address",
            "full_address",
            "phone",
            "email",
        ]

    full_category = CategorySerializer(source="category", read_only=True)

    full_address = serializers.SerializerMethodField(source="address")

    def get_full_address(self, obj):
        obj_addr = {
            "location": obj.location,
            "district": obj.district,
            "address": obj.address,
            "state_code": obj.state_code,
            "zip_code": obj.zip_code,
        }
        return AddressSerializer(obj_addr).data

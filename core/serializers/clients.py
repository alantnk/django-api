from core.models import Client, Category, Contact, Position
from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
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
            "category_detail",
            "idoc",
            "location",
            "state_code",
            "zip_code",
            "district",
            "address",
            "full_address",
            "cover",
            "phone",
            "email",
            "created_at",
            "user",
            "updated_at",
            "editor",
        ]

    district = serializers.CharField(max_length=100, write_only=True, required=False)
    zip_code = serializers.CharField(max_length=10, write_only=True, required=False)
    state_code = serializers.CharField(max_length=3, write_only=True, required=False)
    location = serializers.CharField(max_length=100, write_only=True, required=False)
    address = serializers.CharField(max_length=100, write_only=True, required=False)

    user = serializers.StringRelatedField(read_only=True)
    editor = serializers.StringRelatedField(read_only=True)

    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    category_detail = CategorySerializer(source="category", read_only=True)

    full_address = serializers.SerializerMethodField(source="address", read_only=True)

    def get_full_address(self, obj):
        obj_addr = {
            "location": obj.location,
            "district": obj.district,
            "address": obj.address,
            "state_code": obj.state_code,
            "zip_code": obj.zip_code,
        }
        return AddressSerializer(obj_addr).data


class ClientDetailSerializer(ClientSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "fantasy_name",
            "office_name",
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "full_name",
            "email",
            "client",
            "client_detail",
            "phone",
            "position",
            "position_detail",
            "location",
            "district",
            "address",
            "notes",
            "created_at",
            "user",
            "updated_at",
            "editor",
        ]

    client_detail = ClientDetailSerializer(source="client", read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    editor = serializers.StringRelatedField(read_only=True)

    position_detail = PositionSerializer(source="position", read_only=True)

    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

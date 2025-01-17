from core.models import Client, Category, Contact, Position
from .base import UserSerializer
from rest_framework import serializers


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
            "updated_at",
            "user_detail",
            "user_editor_detail",
        ]
        extra_kwargs = {
            "category": {"write_only": True},
            "district": {"write_only": True},
            "zip_code": {"write_only": True},
            "state_code": {"write_only": True},
            "location": {"write_only": True},
            "address": {"write_only": True},
        }
        read_only_fields = [
            "user_detail",
            "user_editor_detail",
            "updated_at",
            "created_at",
        ]

    category_detail = CategorySerializer(source="category", read_only=True)

    full_address = serializers.SerializerMethodField(source="address", read_only=True)

    user_detail = UserSerializer(source="user", read_only=True)
    user_editor_detail = UserSerializer(source="user_editor", read_only=True)

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
            "client_detail",
            "phone",
            "position_detail",
            "location",
            "district",
            "address",
            "notes",
            "user_detail",
            "user_editor_detail",
            # READ_ONLY
            "created_at",
            "updated_at",
            # WRITE_ONLY
            "client",
            "position",
        ]
        extra_kwargs = {
            "client": {"write_only": True},
            "position": {"write_only": True},
        }
        read_only_fields = [
            "created_at",
            "updated_at",
        ]

    user_detail = UserSerializer(source="user", read_only=True)
    user_editor_detail = UserSerializer(source="user_editor", read_only=True)

    client_detail = ClientDetailSerializer(source="client", read_only=True)

    position_detail = PositionSerializer(source="position", read_only=True)

    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

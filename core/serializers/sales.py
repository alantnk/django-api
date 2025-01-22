from core.models import Sale, SaleHistory
from rest_framework import serializers
from .base import UserSerializer, ClientDetailSerializer


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            "id",
            "estimated_value",
            "chance",
            "status",
            "funnel_stage",
            "expected_date",
            "notes",
            "user_detail",
            "client_detail",
            # READ_ONLY
            "updated_at",
            "created_at",
            # WRITE_ONLY
            "client",
        ]
        read_only_fields = [
            "updated_at",
            "created_at",
        ]

        extra_kwargs = {
            "client": {"write_only": True},
        }

    user_detail = UserSerializer(source="user", read_only=True)
    client_detail = ClientDetailSerializer(source="client", read_only=True)


class SaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleHistory
        fields = "__all__"
        read_only_fields = ["__all__"]

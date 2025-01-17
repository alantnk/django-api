from core.models import Sale, SaleHistory
from rest_framework import serializers
from .base import UserSerializer


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            "id",
            "client",
            "estimated_value",
            "chance",
            "status",
            "funnel_stage",
            "expected_date",
            "user",
            "notes",
            "user_detail",
            "user_editor_detail",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "updated_at",
            "created_at",
        ]

    user_detail = UserSerializer(source="user", read_only=True)


class SaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleHistory
        fields = "__all__"
        read_only_fields = ["__all__"]

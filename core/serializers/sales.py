from core.models import Sale, SaleHistory
from django.conf import settings
from rest_framework import serializers


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
            "created_at",
            "updated_at",
        ]

    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)


class SaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleHistory
        fields = "__all__"
        read_only_fields = ["__all__"]

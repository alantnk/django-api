from core.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ["id", "fantasy_name", "office_name", "category", "idoc", "email"]

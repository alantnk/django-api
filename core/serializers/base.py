from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "fantasy_name",
            "office_name",
        ]

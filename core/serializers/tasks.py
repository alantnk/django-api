from rest_framework import serializers
from core.models import Task, Tag
from .base import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "tags",
            "status",
            "due_date",
            "user_detail",
            "closed",
        ]
        read_only_fields = [
            "closed",
            "updated_at",
            "created_at",
        ]

    user_detail = UserSerializer(source="user", read_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

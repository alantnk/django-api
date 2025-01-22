from rest_framework import serializers
from core.models import Task, Tag
from .base import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            # READ_ONLY
            "user_detail",
            "tag_list",
            "closed",
            "updated_at",
            "created_at",
            # WRITE_ONLY
            "tags",
        ]
        read_only_fields = [
            "closed",
            "updated_at",
            "created_at",
        ]

        extra_kwargs = {
            "tags": {"write_only": True},
        }

    user_detail = UserSerializer(source="user", read_only=True)
    tag_list = TagSerializer(many=True, source="tags", read_only=True)

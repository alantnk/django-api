from rest_framework import serializers
from core.models import Task, Tag


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "user",
            "tags",
            "status",
            "due_date",
            "completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user",
            "updated_at",
            "created_at",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

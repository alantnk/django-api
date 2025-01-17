from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "user",
            "sale",
            "client",
            "status",
            "level",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "updated_at", "created_at"]

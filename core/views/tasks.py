from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Task, Tag
from ..serializers import TaskSerializer, TagSerializer
from ..mixins import OwnerPermissionMixin, SaveUserMixin


class TaskViewSet(SaveUserMixin, OwnerPermissionMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["title, user__username", "tag__name"]
    ordering_fields = ["id", "title", "updated_at"]
    ordering = ["-id"]

    def create(self, request, *args, **kwargs):
        ts = Task.objects.filter(user=request.user, completed=False)
        print(ts)
        if Task.objects.filter(user=request.user, completed=False).exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": ["This user already has a task in progress."],
                }
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if Task.objects.filter(user=request.user, completed=True).exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": ["This user already has a task finished."],
                }
            )
        return super().update(request, *args, **kwargs)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TagSerializer

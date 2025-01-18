from core.permissions import IsOwnerOrAdmin, isOwner
from rest_framework.permissions import IsAuthenticated


class SaveUserMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_editor=self.request.user)
        return super().perform_update(serializer)


class OwnerAdminPermissionMixin:
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]


class OwnerPermissionMixin:
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [isOwner()]
        else:
            return [IsAuthenticated()]

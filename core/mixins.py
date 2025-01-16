from core.permissions import IsOwnerOrAdmin, isOwner
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class SaveUserMixin:
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user)
        return super().perform_update(serializer)


class ClientOwnerPermissionMixin:
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        else:
            return [IsAuthenticated()]


class SaleOwnerPermissionMixin:
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [isOwner()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

from core.permissions import IsOwnerOrAdmin, isOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveUserMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_editor=self.request.user)
        return super().perform_update(serializer)


class AdminDestroyPermissionMixin:

    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]


class OwnerAdminPermissionMixin(AdminDestroyPermissionMixin):
    def get_permissions(self):
        if self.request.method in ["PATCH"]:
            return [IsOwnerOrAdmin()]
        else:
            return super().get_permissions()


class OwnerPermissionMixin(AdminDestroyPermissionMixin):
    def get_permissions(self):
        if self.request.method in ["PATCH"]:
            return [isOwner()]
        else:
            return super().get_permissions()

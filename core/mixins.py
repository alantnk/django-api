from user_control.permisssions import (
    IsOwnerOrAdminControl,
    IsOwnerControl,
    IsAdminControl,
)
from rest_framework.permissions import IsAuthenticated


class SaveUserMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_editor=self.request.user)
        return super().perform_update(serializer)


class AdminDestroyPermissionMixin:

    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAdminControl()]
        else:
            return [IsAuthenticated()]


class OwnerAdminUpdatePermissionMixin(AdminDestroyPermissionMixin):
    def get_permissions(self):
        if self.request.method in ["PATCH"]:
            return [IsOwnerOrAdminControl()]
        else:
            return super().get_permissions()


class OwnerUpdatePermissionMixin(AdminDestroyPermissionMixin):
    def get_permissions(self):
        if self.request.method in ["PATCH"]:
            return [IsOwnerControl()]
        else:
            return super().get_permissions()

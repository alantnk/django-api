from core.permissions import IsOwnerOrAdmin


class SaveUserRequestMixin:
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        else:
            return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user)
        return super().perform_update(serializer)

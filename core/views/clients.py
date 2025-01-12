from core.models import Client
from ..serializers import ClientSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.permissions import IsOwnerOrAdmin


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

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

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-updated_at")
        has_categoryi_id = "category_id" in request.query_params
        if has_categoryi_id:
            category_id = request.query_params["category_id"]
            self.queryset = self.queryset.filter(category_id=category_id)
            return super().list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

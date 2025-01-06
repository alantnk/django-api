from core.models import Client
from ..serializers import ClientSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-updated_at")
        return super().list(request, *args, **kwargs)

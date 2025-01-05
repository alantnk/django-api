from core.models import Client
from ..serializers import ClientSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get"]

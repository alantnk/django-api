from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import ClientOwnerPermissionMixin
from core.models import Sale, SaleHistory
from ..serializers import SaleSerializer, SaleHistorySerializer


class SaleViewSet(ClientOwnerPermissionMixin, ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["client__fantasy_name", "client__office_name"]
    ordering_fields = [
        "id",
        "client__fantasy_name",
        "client__office_name",
        "updated_at",
    ]
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

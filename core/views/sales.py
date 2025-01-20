from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import OwnerPermissionMixin
from core.models import Sale, SaleHistory
from ..serializers import SaleSerializer, SaleHistorySerializer


class SaleViewSet(OwnerPermissionMixin, ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["client__fantasy_name", "client__office_name", "user__username"]
    ordering_fields = [
        "id",
        "client__fantasy_name",
        "client__office_name",
        "updated_at",
    ]
    ordering = ["-id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SaleHistoryViewSet(ModelViewSet):
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAdminUser]  # MUDAR PARA IS_ADMIN_USER
    serializer_class = SaleHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = [
        "id",
        "client__fantasy_name",
        "client__office_name",
        "changed_at",
    ]
    ordering = ["-id"]

    http_method_names = ["get", "head", "options"]

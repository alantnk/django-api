from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import OwnerUpdatePermissionMixin
from core.models import Sale, SaleHistory
from user_control.permisssions import IsAdminControl
from ..serializers import SaleSerializer, SaleHistorySerializer


class SaleViewSet(OwnerUpdatePermissionMixin, ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["client__fantasy_name", "client__office_name", "user__username"]
    filterset_fields = ["client_id", "user_id", "status"]
    ordering_fields = [
        "id",
        "client__fantasy_name",
        "client__office_name",
        "expected_date",
        "updated_at",
    ]
    ordering = ["-id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == "admin":
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        if Sale.objects.filter(pk=kwargs["pk"], closed=True).exists():
            raise serializers.ValidationError(
                {"sale_error": ["This sale is already closed."]}
            )
        return super().partial_update(request, *args, **kwargs)


class SaleHistoryViewSet(ReadOnlyModelViewSet):
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAdminControl]
    serializer_class = SaleHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["sale_id", "user_id"]
    ordering_fields = [
        "id",
        "client__fantasy_name",
        "client__office_name",
        "changed_at",
    ]
    ordering = ["-id"]

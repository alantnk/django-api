from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import ClientOwnerPermissionMixin, SaveUserMixin
from core.models import Client, Contact, Category, Position
from ..serializers import (
    ClientSerializer,
    ContactSerializer,
    CategorySerializer,
    PositionSerializer,
)


class ClientViewSet(SaveUserMixin, ClientOwnerPermissionMixin, ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["fantasy_name", "office_name"]
    filterset_fields = ["category_id"]
    ordering_fields = ["id", "fantasy_name", "office_name", "updated_at"]
    ordering = ["-id"]


class ContactViewSet(SaveUserMixin, ClientOwnerPermissionMixin, ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["full_name"]
    filterset_fields = ["client_id", "position_id"]
    ordering_fields = ["id", "full_name", "updated_at"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["name"]
    ordering_fields = ["id", "name", "updated_at"]
    ordering = ["-id"]


class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["name"]
    ordering_fields = ["id", "name", "updated_at"]
    ordering = ["-id"]

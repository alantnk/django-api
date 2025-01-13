from core.mixins import SaveUserRequestMixin
from core.models import Client, Contact
from ..serializers import ClientSerializer, ContactSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(SaveUserRequestMixin, ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-updated_at")
        if "order_by" in request.query_params:
            order_by = request.query_params["order_by"]
            self.queryset = self.queryset.order_by(order_by)

        if "category_id" in request.query_params:
            category_id = request.query_params["category_id"]
            self.queryset = self.queryset.filter(category_id=category_id)
            return super().list(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)


class ContactViewSet(SaveUserRequestMixin, ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-updated_at")
        if "order_by" in request.query_params:
            order_by = request.query_params["order_by"]
            self.queryset = self.queryset.order_by(order_by)

        if "client_id" in request.query_params:
            client_id = request.query_params["client_id"]
            self.queryset = self.queryset.filter(client_id=client_id)

        if "position_id" in request.query_params:
            position_id = request.query_params["position_id"]
            self.queryset = self.queryset.filter(position_id=position_id)

        return super().list(request, *args, **kwargs)

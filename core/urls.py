from django.urls import path

from core.views import ClientViewSet, ContactViewSet
from .views.base import *
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "core"

clients_router = SimpleRouter()
clients_router.register("clients", ClientViewSet, basename="clients-api")

contacts_router = SimpleRouter()
contacts_router.register("contacts", ContactViewSet, basename="contacts-api")

urlpatterns = [
    # Auth Routes
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Public Routes
    path("ping/", PingView.as_view(), name="ping"),
    path("", ApiPageView.as_view()),
]

urlpatterns += clients_router.urls
urlpatterns += contacts_router.urls

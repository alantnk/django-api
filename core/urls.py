from django.urls import path

from core.views import ClientViewSet
from .views.base import *
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

clients_router = SimpleRouter()
clients_router.register("clients", ClientViewSet, basename="clients-api")

urlpatterns = [
    # Auth Routes
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Public Routes
    path("ping/", PingView.as_view()),
    path("", ApiPageView.as_view()),
]

urlpatterns += clients_router.urls

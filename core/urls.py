from django.urls import path

from core.views import ClientViewSet
from .views.base import *
from rest_framework.routers import SimpleRouter

clients_router = SimpleRouter()
clients_router.register("clients", ClientViewSet, basename="clients-api")

urlpatterns = [
    # Public Routes
    path("ping/", PingView.as_view()),
    path("", ApiPageView.as_view()),
]

urlpatterns += clients_router.urls

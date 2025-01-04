from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response


class ApiPageView(TemplateView):
    template_name = "index.html"


class PingView(APIView):
    def get(self, request):
        return Response({"status": "PONG"})

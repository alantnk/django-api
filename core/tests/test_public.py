from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.views import ApiPageView, PingView


class PingViewTest(APITestCase):
    def test_ping(self):
        response = self.client.get(reverse("core:ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PingView)
        self.assertEqual(response.json(), {"status": "PONG"})


class ApiPageViewTest(APITestCase):
    def test_api_page(self):
        response = self.client.get(reverse("core:api_index"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.context_data["view"], ApiPageView)
        self.assertTemplateUsed(response, "api_index.html")

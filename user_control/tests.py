from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from model_bakery import baker

from .views import UserViewSet

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.APIClient = APIClient()
        self.basic_user = baker.make(User, is_staff=False, is_superuser=False)
        return super().setUp()

    def test_get_info(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        resp = self.APIClient.get("/auth/u/info/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.renderer_context["view"], UserViewSet)
        self.assertEqual(resp.data["username"], self.basic_user.username)
        self.assertEqual(resp.data["email"], self.basic_user.email)

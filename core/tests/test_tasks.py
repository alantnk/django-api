from rest_framework.test import force_authenticate
from rest_framework import status
from .base import BaseTestCase
from core.views import TaskViewSet, TagViewSet


class TaskTest(BaseTestCase):
    def list_tasks_by_user(self):
        force_authenticate(self.client, user=self.simple_user)
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

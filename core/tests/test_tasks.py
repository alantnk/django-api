import random
from rest_framework.test import force_authenticate
from rest_framework import status
from .base import BaseTestCase
from core.views import TaskViewSet, TagViewSet


class TaskTest(BaseTestCase):
    def test_list_tasks_by_user(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_task(user=self.simple_user)
        req = self.factory.get("/api/tasks/")
        force_authenticate(req, user=self.simple_user)
        response = TaskViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["count"], count)

    def test_status_unauthorized(self):
        req = self.factory.get("/api/tasks/")
        response = TaskViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks_by_admin_user(self):
        for _ in range(5):
            self.make_task(user=self.simple_user)
        self.make_task(user=self.staff_user)
        req = self.factory.get("/api/tasks/")
        force_authenticate(req, user=self.staff_user)
        response = TaskViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["count"], 6)

    def test_retrieve_task(self):
        task = self.make_task(user=self.simple_user)
        req = self.factory.get("/api/tasks/")
        force_authenticate(req, user=self.simple_user)
        response = TaskViewSet.as_view({"get": "retrieve"})(req, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["id"], task.id)

    def test_create_task(self):
        task_obj = {
            "title": "test",
            "description": "test",
            "tags": [self.make_tag().id],
            "user": self.simple_user.id,
        }
        req = self.factory.post("/api/tasks/", task_obj, format="json")
        force_authenticate(req, user=self.simple_user)
        response = TaskViewSet.as_view({"post": "create"})(req)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["title"], task_obj["title"])

    def test_update_task(self):
        task = self.make_task(user=self.simple_user)
        new_status = "done"
        req = self.factory.patch(
            "/api/tasks/",
            {
                "status": new_status,
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = TaskViewSet.as_view({"patch": "partial_update"})(req, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["id"], task.id)
        self.assertEqual(response.data["status"], new_status)

    def test_destroy_task(self):
        task = self.make_task(user=self.staff_user)
        req = self.factory.delete("/api/tasks/")
        force_authenticate(req, user=self.staff_user)
        response = TaskViewSet.as_view({"delete": "destroy"})(req, pk=task.id)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)

    def test_list_tasks_by_search_username(self):
        for _ in range(5):
            self.make_task(user=self.super_user)
        self.make_task(user=self.staff_user)
        req = self.factory.get(f"/api/tasks?username={self.super_user.username}")
        force_authenticate(req, user=self.staff_user)
        response = TaskViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["count"], 6)

    def test_list_tasks_by_query_tags_id(self):
        spam_tag = self.make_tag()
        bacon_tag = self.make_tag()
        eggs_tag = self.make_tag()
        for i in range(20):
            if i < 5:
                self.make_task(user=self.staff_user, tags=[spam_tag])
            elif i < 10:
                self.make_task(user=self.staff_user, tags=[bacon_tag])
            else:
                self.make_task(user=self.staff_user, tags=[bacon_tag, eggs_tag])

        req = self.factory.get(f"/api/tasks?tags=8")
        force_authenticate(req, user=self.staff_user)
        response = TaskViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TaskViewSet)
        self.assertEqual(response.data["count"], 10)


class TagTest(BaseTestCase):
    def test_list_tags(self):
        count = 50
        for _ in range(count):
            self.make_tag()
        req = self.factory.get("/api/tags/")
        force_authenticate(req, user=self.staff_user)
        response = TagViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)
        self.assertEqual(response.data["count"], count)

    def test_status_unauthorized(self):
        req = self.factory.get("/api/tags/")
        response = TagViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_tag(self):
        tag = self.make_tag()
        req = self.factory.get("/api/tags/")
        force_authenticate(req, user=self.staff_user)
        response = TagViewSet.as_view({"get": "retrieve"})(req, pk=tag.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)
        self.assertEqual(response.data["id"], tag.id)

    def test_create_tag(self):
        tag_obj = {"name": "test"}
        req = self.factory.post("/api/tags/", tag_obj, format="json")
        force_authenticate(req, user=self.staff_user)
        response = TagViewSet.as_view({"post": "create"})(req)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)
        self.assertEqual(response.data["name"], tag_obj["name"])

    def test_update_tag(self):
        tag = self.make_tag()
        new_name = "ipsum"
        req = self.factory.patch(
            "/api/tags/",
            {
                "name": new_name,
            },
            format="json",
        )
        force_authenticate(req, user=self.staff_user)
        response = TagViewSet.as_view({"patch": "partial_update"})(req, pk=tag.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)
        self.assertEqual(response.data["id"], tag.id)
        self.assertEqual(response.data["name"], new_name)

    def test_destroy_tag(self):
        tag = self.make_tag()
        req = self.factory.delete("/api/tags/")
        force_authenticate(req, user=self.staff_user)
        response = TagViewSet.as_view({"delete": "destroy"})(req, pk=tag.id)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], TagViewSet)

    def test_simple_user_forbidden_create(self):
        tag_obj = {"name": "ipsum"}
        req = self.factory.post("/api/tags/", tag_obj, format="json")
        force_authenticate(req, user=self.simple_user)
        response = TagViewSet.as_view({"post": "create"})(req)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_simple_user_forbidden_update(self):
        tag = self.make_tag()
        new_name = "ipsum"
        req = self.factory.patch(
            "/api/tags/",
            {
                "name": new_name,
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = TagViewSet.as_view({"patch": "partial_update"})(req, pk=tag.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_simple_user_forbidden_retrieve(self):
        tag = self.make_tag()
        req = self.factory.get("/api/tags/")
        force_authenticate(req, user=self.simple_user)
        response = TagViewSet.as_view({"get": "retrieve"})(req, pk=tag.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

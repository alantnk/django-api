import random
from rest_framework.test import force_authenticate
from rest_framework import status
from .base import BaseTestCase
from core.views import TaskViewSet


class TaskTest(BaseTestCase):
    def test_list_tasks_by_user(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_task(user=self.basic_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)

    def test_status_unauthorized(self):
        response = self.APIClient.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks_by_admin_user(self):
        for _ in range(5):
            self.make_task(user=self.basic_user)
        self.make_task(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)

    def test_retrieve_task(self):
        task = self.make_task(user=self.basic_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.get(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], task.id)

    def test_create_task(self):
        task_obj = {
            "title": "test",
            "description": "test",
            "tags": [self.make_tag().id],
            "user": self.basic_user.id,
        }
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.post("/api/tasks/", task_obj, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], task_obj["title"])

    def test_update_task(self):
        task = self.make_task(user=self.basic_user)
        new_status = "done"
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.patch(
            f"/api/tasks/{task.id}/", {"status": new_status}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], task.id)
        self.assertEqual(response.data["status"], new_status)

    def test_destroy_task(self):
        task = self.make_task(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_tasks_by_search_username(self):
        view = TaskViewSet.as_view({"get": "list"})
        for _ in range(5):
            self.make_task(user=self.super_user)
        self.make_task(user=self.admin_user)
        request = self.factory.get(
            f"/api/tasks?username={self.super_user.username}",
            content_type="application/json",
        )
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 6)

    def test_list_tasks_by_query_tags_id(self):
        spam_tag = self.make_tag()
        bacon_tag = self.make_tag()
        eggs_tag = self.make_tag()
        cheese_tag = self.make_tag()
        self.make_task(user=self.basic_user, tags=[spam_tag, cheese_tag])
        for i in range(20):
            if i <= 1:
                self.make_task(user=self.admin_user, tags=[spam_tag])
            elif 1 < i < 19:
                self.make_task(user=self.admin_user, tags=[bacon_tag])
            else:
                self.make_task(user=self.admin_user, tags=[eggs_tag])

        view = TaskViewSet.as_view({"get": "list"})
        request = self.factory.get(
            f"/api/tasks?tags={spam_tag.id},{eggs_tag.id}",
            content_type="application/json",
        )
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 4)

    def test_not_update_task_closed(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        task = self.make_task(user=self.admin_user, closed=True)
        resp = self.APIClient.patch(
            f"/api/tasks/{task.id}/",
            {"description": "test description"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_multiple_task(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        self.APIClient.post(
            "/api/tasks/",
            {
                "title": "test title",
                "description": "test description",
                "tags": [self.make_tag().id],
            },
            format="json",
        )
        resp = self.APIClient.post(
            "/api/tasks/",
            {
                "title": "test title",
                "description": "test description",
                "tags": [self.make_tag().id],
            },
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class TagTest(BaseTestCase):
    def test_list_tags(self):
        count = 50
        for _ in range(count):
            self.make_tag()
        self.APIClient.force_authenticate(user=self.admin_user)
        resp = self.APIClient.get("/api/tags/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["count"], count)

    def test_status_unauthorized(self):
        resp = self.APIClient.get("/api/tags/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_tag(self):
        tag = self.make_tag()
        self.APIClient.force_authenticate(user=self.admin_user)
        resp = self.APIClient.get(f"/api/tags/{tag.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], tag.id)

    def test_create_tag(self):
        tag_obj = {"name": "test"}
        self.APIClient.force_authenticate(user=self.admin_user)
        resp = self.APIClient.post("/api/tags/", tag_obj, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["name"], tag_obj["name"].upper())

    def test_update_tag(self):
        tag = self.make_tag()
        new_name = "ipsum"
        self.APIClient.force_authenticate(user=self.admin_user)
        resp = self.APIClient.patch(
            f"/api/tags/{tag.id}/",
            {
                "name": new_name,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], tag.id)
        self.assertEqual(resp.data["name"], new_name.upper())

    def test_destroy_tag(self):
        tag = self.make_tag()
        self.APIClient.force_authenticate(user=self.admin_user)
        resp = self.APIClient.delete(f"/api/tags/{tag.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_basic_user_forbidden_create(self):
        tag_obj = {"name": "ipsum"}
        self.APIClient.force_authenticate(user=self.basic_user)
        resp = self.APIClient.post("/api/tags/", tag_obj, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_basic_user_forbidden_update(self):
        tag = self.make_tag()
        new_name = "ipsum"
        self.APIClient.force_authenticate(user=self.basic_user)
        resp = self.APIClient.patch(
            f"/api/tags/{tag.id}/",
            {
                "name": new_name,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_basic_user_forbidden_retrieve(self):
        tag = self.make_tag()
        self.APIClient.force_authenticate(user=self.basic_user)
        resp = self.APIClient.get(f"/api/tags/{tag.id}/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

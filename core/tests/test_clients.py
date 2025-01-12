import pytest
import random
from rest_framework.test import force_authenticate
from rest_framework import status

from django.urls import reverse
from .api_test_base import APITestBase
from core.views import ClientViewSet


class ClientTest(APITestBase):

    @pytest.mark.skip
    def test_ping(self):
        response = self.client.get(reverse("core:ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "PONG"})

    def test_status_unauthorized(self):
        client = self.make_client()
        retrieve_client_req = self.factory.get("/api/clients/")
        create_client_req = self.factory.post(
            "/api/clients/", self.client_post_obj, format="json"
        )
        update_client_req = self.factory.patch(
            "/api/clients/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        destroy_client_req = self.factory.delete("/api/clients/")

        retrieve_client_response = ClientViewSet.as_view({"get": "retrieve"})(
            retrieve_client_req, pk=client.id
        )
        create_client_response = ClientViewSet.as_view({"post": "create"})(
            create_client_req
        )
        update_client_response = ClientViewSet.as_view({"patch": "partial_update"})(
            update_client_req, pk=client.id
        )
        destroy_client_response = ClientViewSet.as_view({"delete": "destroy"})(
            destroy_client_req, pk=client.id
        )

        self.assertListEqual(
            [
                retrieve_client_response.status_code,
                create_client_response.status_code,
                update_client_response.status_code,
                destroy_client_response.status_code,
            ],
            [status.HTTP_401_UNAUTHORIZED for _ in range(4)],
        )

    def test_list_clients(self):
        count = 50
        for i in range(count):
            self.make_client()
        req = self.factory.get("/api/clients/")
        force_authenticate(req, user=self.user)
        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)
        self.assertEqual(len(response.data["results"]), 10)

    def test_retrieve_client(self):
        client = self.make_client()
        req = self.factory.get("/api/clients/")
        force_authenticate(req, user=self.user)
        response = ClientViewSet.as_view({"get": "retrieve"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], client.id)

    def test_create_client(self):
        req = self.factory.post(
            "/api/clients/",
            self.client_post_obj,
            format="json",
        )
        force_authenticate(req, user=self.user)
        response = ClientViewSet.as_view({"post": "create"})(req)
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["office_name"], self.client_post_obj["office_name"].upper()
        )

    def test_update_client(self):
        client = self.make_client(created_by=self.user)
        new_email = "lorem.ipsum@example.com"
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": new_email,
            },
            format="json",
        )
        force_authenticate(req, user=self.user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], client.id)
        self.assertEqual(response.data["email"], new_email)

    def test_delete_client(self):
        client = self.make_client(created_by=self.user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_clients_by_category_id(self):
        category = self.make_category()
        for i in range(10):
            if i > random.randint(0, 9):
                self.make_client(category=category)
            else:
                self.make_client()
        req = self.factory.get(f"/api/clients/?category_id={category.id}")
        force_authenticate(req, user=self.user)

        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][-1]["category"], category.id)

    def test_user_forbidden_update_client(self):
        client = self.make_client(created_by=self.user)
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.not_staff_user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_forbidden_delete_client(self):
        client = self.make_client(created_by=self.user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.not_staff_user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_update_client(self):
        client = self.make_client(created_by=self.not_staff_user)
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.admin_user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_delete_client(self):
        client = self.make_client(created_by=self.not_staff_user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.admin_user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

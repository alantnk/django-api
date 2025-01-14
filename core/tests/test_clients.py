import pytest
import random
from rest_framework.test import force_authenticate, APITestCase
from rest_framework import status

from django.urls import reverse
from .api_test_base import BaseTestCase
from core.views import ClientViewSet, ContactViewSet


class PingViewTest(APITestCase):
    @pytest.mark.skip
    def test_ping(self):
        response = self.client.get(reverse("core:ping"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "PONG"})


class ClientTest(BaseTestCase):

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

    def test_list_client_by_category_id(self):
        category = self.make_category()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_client(category=category)
            else:
                self.make_client()
        req = self.factory.get(f"/api/clients/?category_id={category.id}")
        force_authenticate(req, user=self.user)

        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["category"], category.id)

    def test_order_list_client_by_office_name(self):
        name = "BACON POTATO"
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_client(office_name=name)
            else:
                self.make_client(office_name="NOT " + name)
        req = self.factory.get(f"/api/clients/?ordering=office_name")
        force_authenticate(req, user=self.user)

        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["office_name"], name)

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


class ContactTest(BaseTestCase):

    def test_list_contacts(self):
        count = random.randint(1, 20)
        for _ in range(count):
            self.make_contact()
        req = self.factory.get("/api/contacts/")
        force_authenticate(req, user=self.user)
        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_contact(self):
        contact = self.make_contact()
        req = self.factory.get("/api/contacts/")
        force_authenticate(req, user=self.user)
        response = ContactViewSet.as_view({"get": "retrieve"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], contact.id)

    def test_create_contact(self):
        client = self.make_client()
        req = self.factory.post(
            "/api/contacts/",
            {
                "full_name": "Jack Smith",
                "email": "matrix@example.com",
                "client": client.id,
            },
            format="json",
        )
        force_authenticate(req, user=self.user)
        response = ContactViewSet.as_view({"post": "create"})(req)
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)

    def test_update_contact(self):

        contact = self.make_contact(created_by=self.user)
        new_email = "lorem.ipsum@example.com"
        req = self.factory.patch(
            "/api/contacts/",
            {
                "email": new_email,
            },
            format="json",
        )
        force_authenticate(req, user=self.user)
        response = ContactViewSet.as_view({"patch": "partial_update"})(
            req, pk=contact.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], contact.id)
        self.assertEqual(response.data["email"], new_email)

    def test_delete_contact(self):
        contact = self.make_contact(created_by=self.user)
        req = self.factory.delete("/api/contacts/")
        force_authenticate(req, user=self.user)
        response = ContactViewSet.as_view({"delete": "destroy"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_status_unauthorized(self):
        contact = self.make_contact()
        retrieve_contact_req = self.factory.get("/api/contacts/")
        update_contact_req = self.factory.patch(
            "/api/contacts/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        destroy_contact_req = self.factory.delete("/api/contacts/")

        retrieve_contact_response = ContactViewSet.as_view({"get": "retrieve"})(
            retrieve_contact_req, pk=contact.id
        )
        update_contact_response = ContactViewSet.as_view({"patch": "partial_update"})(
            update_contact_req, pk=contact.id
        )
        destroy_contact_response = ContactViewSet.as_view({"delete": "destroy"})(
            destroy_contact_req, pk=contact.id
        )

        self.assertListEqual(
            [
                retrieve_contact_response.status_code,
                update_contact_response.status_code,
                destroy_contact_response.status_code,
            ],
            [status.HTTP_401_UNAUTHORIZED for _ in range(3)],
        )

    def test_list_contacts_by_client_id(self):
        client = self.make_client()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(client=client)
            else:
                self.make_contact()
        req = self.factory.get(f"/api/contacts/?client_id={client.id}")
        force_authenticate(req, user=self.user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["client"], client.id)

    def test_list_contacts_by_position_id(self):
        position = self.make_position()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(position=position)
            else:
                self.make_contact()
        req = self.factory.get(f"/api/contacts/?position_id={position.id}")
        force_authenticate(req, user=self.user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["position"], position.id)

    def test_order_list_contact_by_full_name(self):
        name = "lorem ipsum"
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(full_name=name)
            else:
                self.make_contact(full_name="NOT " + name)
        req = self.factory.get(f"/api/contacts/?ordering=full_name")
        force_authenticate(req, user=self.user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["full_name"], name)

    def test_forbidden_update_contact(self):
        contact = self.make_contact(created_by=self.user)
        req = self.factory.patch(
            "/api/contacts/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.not_staff_user)
        response = ContactViewSet.as_view({"patch": "partial_update"})(
            req, pk=contact.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_delete_contact(self):
        contact = self.make_contact(created_by=self.user)
        req = self.factory.delete("/api/contacts/")
        force_authenticate(req, user=self.not_staff_user)
        response = ContactViewSet.as_view({"delete": "destroy"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

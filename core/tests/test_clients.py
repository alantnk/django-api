import random
from rest_framework.test import force_authenticate
from rest_framework import status


from .base import BaseTestCase
from core.views import ClientViewSet, ContactViewSet, CategoryViewSet, PositionViewSet


class ClientTest(BaseTestCase):

    def test_list_clients(self):
        count = 50
        for i in range(count):
            self.make_client()
        req = self.factory.get("/api/clients/")
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ClientViewSet)

        self.assertEqual(response.data["count"], count)
        self.assertEqual(len(response.data["results"]), 10)

    def test_retrieve_client(self):
        client = self.make_client()
        req = self.factory.get("/api/clients/")
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"get": "retrieve"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ClientViewSet)

        self.assertEqual(response.data["id"], client.id)

    def test_create_client(self):
        req = self.factory.post(
            "/api/clients/",
            self.client_post_obj,
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"post": "create"})(req)
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], ClientViewSet)

        self.assertEqual(
            response.data["office_name"], self.client_post_obj["office_name"].upper()
        )

    def test_update_client(self):
        client = self.make_client(user=self.simple_user)
        new_email = "lorem.ipsum@example.com"
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": new_email,
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ClientViewSet)

        self.assertEqual(response.data["id"], client.id)
        self.assertEqual(response.data["email"], new_email)

    def test_delete_client(self):
        client = self.make_client(user=self.staff_user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.staff_user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], ClientViewSet)

    def test_status_unauthorized(self):
        client = self.make_client()
        retrieve_client_req = self.factory.get("/api/clients/")

        retrieve_client_response = ClientViewSet.as_view({"get": "retrieve"})(
            retrieve_client_req, pk=client.id
        )

        self.assertEqual(
            retrieve_client_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_client_by_category_id(self):
        category = self.make_category()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_client(category=category)
            else:
                self.make_client()
        req = self.factory.get(f"/api/clients?category_id={category.id}")
        force_authenticate(req, user=self.simple_user)

        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(
            response.data["results"][0]["category_detail"]["id"], category.id
        )

    def test_order_list_client_by_office_name(self):
        name = "BACON POTATO"
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_client(office_name=name)
            else:
                self.make_client(office_name="NOT " + name)
        req = self.factory.get(f"/api/clients?ordering=office_name")
        force_authenticate(req, user=self.simple_user)

        response = ClientViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["office_name"], name)

    def test_user_forbidden_update_client(self):
        client = self.make_client(user=self.staff_user)
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_forbidden_delete_client(self):
        client = self.make_client(user=self.staff_user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.simple_user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_update_client(self):
        client = self.make_client(user=self.simple_user)
        req = self.factory.patch(
            "/api/clients/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.staff_user)
        response = ClientViewSet.as_view({"patch": "partial_update"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_delete_client(self):
        client = self.make_client(user=self.simple_user)
        req = self.factory.delete("/api/clients/")
        force_authenticate(req, user=self.staff_user)
        response = ClientViewSet.as_view({"delete": "destroy"})(req, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ContactTest(BaseTestCase):

    def test_list_contacts(self):
        count = random.randint(1, 20)
        for _ in range(count):
            self.make_contact()
        req = self.factory.get("/api/contacts/")
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ContactViewSet)

        self.assertEqual(response.data["count"], count)

    def test_retrieve_contact(self):
        contact = self.make_contact()
        req = self.factory.get("/api/contacts/")
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"get": "retrieve"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ContactViewSet)

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
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"post": "create"})(req)
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], ContactViewSet)

    def test_update_contact(self):

        contact = self.make_contact(user=self.simple_user)
        new_email = "lorem.ipsum@example.com"
        req = self.factory.patch(
            "/api/contacts/",
            {
                "email": new_email,
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"patch": "partial_update"})(
            req, pk=contact.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], ContactViewSet)

        self.assertEqual(response.data["id"], contact.id)
        self.assertEqual(response.data["email"], new_email)

    def test_delete_contact(self):
        contact = self.make_contact(user=self.staff_user)
        req = self.factory.delete("/api/contacts/")
        force_authenticate(req, user=self.staff_user)
        response = ContactViewSet.as_view({"delete": "destroy"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], ContactViewSet)

    def test_status_unauthorized(self):

        contact = self.make_contact()
        retrieve_contact_req = self.factory.get("/api/contacts/")

        retrieve_contact_response = ContactViewSet.as_view({"get": "retrieve"})(
            retrieve_contact_req, pk=contact.id
        )

        self.assertEqual(
            retrieve_contact_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_contacts_by_client_id(self):
        client = self.make_client()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(client=client)
            else:
                self.make_contact()
        req = self.factory.get(f"/api/contacts?client_id={client.id}")
        force_authenticate(req, user=self.simple_user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["client_detail"]["id"], client.id)

    def test_list_contacts_by_position_id(self):
        position = self.make_position()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(position=position)
            else:
                self.make_contact()
        req = self.factory.get(f"/api/contacts?position_id={position.id}")
        force_authenticate(req, user=self.simple_user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(
            response.data["results"][0]["position_detail"]["id"], position.id
        )

    def test_order_list_contact_by_full_name(self):
        name = "lorem ipsum"
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(full_name=name)
            else:
                self.make_contact(full_name="NOT " + name)
        req = self.factory.get(f"/api/contacts?ordering=full_name")
        force_authenticate(req, user=self.simple_user)

        response = ContactViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.data["results"][0]["full_name"], name)

    def test_forbidden_update_contact(self):
        contact = self.make_contact(user=self.staff_user)
        req = self.factory.patch(
            "/api/contacts/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"patch": "partial_update"})(
            req, pk=contact.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_delete_contact(self):
        contact = self.make_contact(user=self.staff_user)
        req = self.factory.delete("/api/contacts/")
        force_authenticate(req, user=self.simple_user)
        response = ContactViewSet.as_view({"delete": "destroy"})(req, pk=contact.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PositionTest(BaseTestCase):
    def test_list_positions(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_position()
        req = self.factory.get("/api/positions/")
        force_authenticate(req, user=self.simple_user)
        response = PositionViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_position(self):
        position = self.make_position()
        req = self.factory.get("/api/positions/")
        force_authenticate(req, user=self.simple_user)
        response = PositionViewSet.as_view({"get": "retrieve"})(req, pk=position.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["id"], position.id)

    def test_update_position(self):
        position = self.make_position()
        new_name = "ipsum"
        req = self.factory.patch(
            "/api/positions/",
            {
                "name": new_name,
            },
            format="json",
        )
        force_authenticate(req, user=self.staff_user)
        response = PositionViewSet.as_view({"patch": "partial_update"})(
            req, pk=position.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["name"], new_name)

    def test_destroy_position(self):
        position = self.make_position()
        req = self.factory.delete("/api/positions/")
        force_authenticate(req, user=self.staff_user)
        response = PositionViewSet.as_view({"delete": "destroy"})(req, pk=position.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)

    def test_simple_user_forbidden_destroy_position(self):
        position = self.make_position()
        req = self.factory.delete("/api/positions/")
        force_authenticate(req, user=self.simple_user)
        response = PositionViewSet.as_view({"delete": "destroy"})(req, pk=position.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryTest(BaseTestCase):
    def test_list_categories(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_category()
        req = self.factory.get("/api/categories/")
        force_authenticate(req, user=self.simple_user)
        response = CategoryViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_category(self):
        category = self.make_category()
        req = self.factory.get("/api/categories/")
        force_authenticate(req, user=self.simple_user)
        response = CategoryViewSet.as_view({"get": "retrieve"})(req, pk=category.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["id"], category.id)

    def test_create_category(self):
        category_obj = {
            "name": "ipsum",
        }
        req = self.factory.post("/api/categories/", category_obj, format="json")
        force_authenticate(req, user=self.simple_user)
        response = CategoryViewSet.as_view({"post": "create"})(req)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["name"], category_obj["name"])

    def test_update_category(self):
        category = self.make_category()
        new_name = "ipsum"
        req = self.factory.patch(
            "/api/categories/",
            {
                "name": new_name,
            },
            format="json",
        )
        force_authenticate(req, user=self.simple_user)
        response = CategoryViewSet.as_view({"patch": "partial_update"})(
            req, pk=category.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["name"], new_name)

    def test_destroy_category(self):
        category = self.make_category()
        req = self.factory.delete("/api/categories/")
        force_authenticate(req, user=self.staff_user)
        response = CategoryViewSet.as_view({"delete": "destroy"})(req, pk=category.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)

    def test_simple_user_forbidden_destroy_category(self):
        category = self.make_category()
        req = self.factory.delete("/api/categories/")
        force_authenticate(req, user=self.simple_user)
        response = CategoryViewSet.as_view({"delete": "destroy"})(req, pk=category.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

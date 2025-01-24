import random
from rest_framework.test import force_authenticate
from rest_framework import status


from .base import BaseTestCase
from core.views import ClientViewSet, ContactViewSet, CategoryViewSet, PositionViewSet


class ClientTest(BaseTestCase):

    def test_list_clients(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        count = 50
        for i in range(count):
            self.make_client()
        response = self.APIClient.get("/api/clients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)
        self.assertEqual(len(response.data["results"]), 10)

    def test_retrieve_client(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        client = self.make_client()
        response = self.APIClient.get(f"/api/clients/{client.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], client.id)

    def test_create_client(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.post(
            "/api/clients/", self.client_post_obj, format="json"
        )
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["office_name"], self.client_post_obj["office_name"].upper()
        )

    def test_update_client(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        client = self.make_client(user=self.basic_user)
        new_email = "lorem.ipsum@example.com"
        response = self.APIClient.patch(
            f"/api/clients/{client.id}/", {"email": new_email}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], client.id)
        self.assertEqual(response.data["email"], new_email)

    def test_destroy_client(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        client = self.make_client(user=self.basic_user)
        response = self.APIClient.delete(f"/api/clients/{client.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_status_unauthorized(self):
        client = self.make_client()
        response = self.APIClient.get(f"/api/clients/{client.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_client_by_category_id(self):
        category = self.make_category()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_client(category=category)
            else:
                self.make_client()
        view = ClientViewSet.as_view({"get": "list"})
        request = self.factory.get(f"/api/clients?category_id={category.id}")
        force_authenticate(request, user=self.basic_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        view = ClientViewSet.as_view({"get": "list"})
        request = self.factory.get(f"/api/clients?ordering=office_name")
        force_authenticate(request, user=self.basic_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["office_name"], name)

    def test_forbidden_basic_owner_update_client(self):
        client = self.make_client(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.patch(
            f"/api/clients/{client.id}/",
            {"email": "lorem.ipsum@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_basic_owner_destroy_client(self):
        client = self.make_client(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.delete(f"/api/clients/{client.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_update_client(self):
        client = self.make_client(user=self.basic_user)
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.patch(
            f"/api/clients/{client.id}/",
            {"email": "lorem.ipsum@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContactTest(BaseTestCase):

    def test_list_contacts(self):
        count = random.randint(1, 20)
        for _ in range(count):
            self.make_contact()
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.get("/api/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_contact(self):
        contact = self.make_contact()
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.get(f"/api/contacts/{contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], contact.id)

    def test_create_contact(self):
        client = self.make_client()
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.post(
            "/api/contacts/",
            {
                "full_name": "Jack Smith",
                "email": "matrix@example.com",
                "client": client.id,
            },
            format="json",
        )
        self.assertContains(response, "id", status_code=status.HTTP_201_CREATED)

    def test_update_contact(self):
        contact = self.make_contact(user=self.basic_user)
        new_email = "lorem.ipsum@example.com"
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.patch(
            f"/api/contacts/{contact.id}/",
            {
                "email": new_email,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], contact.id)
        self.assertEqual(response.data["email"], new_email)

    def test_destroy_contact(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        contact = self.make_contact(user=self.admin_user)
        response = self.APIClient.delete(f"/api/contacts/{contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_status_unauthorized(self):
        contact = self.make_contact()
        response = self.APIClient.get(f"/api/contacts/{contact.id}/")
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_contacts_by_client_id(self):
        client = self.make_client()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(client=client)
            else:
                self.make_contact()
        view = ContactViewSet.as_view({"get": "list"})
        request = self.factory.get(f"/api/contacts?client_id={client.id}")
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.data["results"][0]["client_detail"]["id"], client.id)

    def test_list_contacts_by_position_id(self):
        position = self.make_position()
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(position=position)
            else:
                self.make_contact()
        view = ContactViewSet.as_view({"get": "list"})
        request = self.factory.get(f"/api/contacts?position_id={position.id}")
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(
            response.data["results"][0]["position_detail"]["id"], position.id
        )

    def test_search_list_contact_by_full_name(self):
        name = "lorem ipsum"
        for i in range(10):
            if i < random.randint(0, 9):
                self.make_contact(full_name="NOT " + name, user=self.admin_user)
            else:
                self.make_contact(full_name=name, user=self.basic_user)
        view = ContactViewSet.as_view({"get": "list"})
        request = self.factory.get(f"/api/contacts?search={name}")
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.data["results"][0]["full_name"], name)

    def test_forbidden_basic_not_owner_update_contact(self):
        contact = self.make_contact(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.patch(
            f"/api/contacts/{contact.id}/",
            {
                "email": "lorem.ipsum@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_basic_user_delete_contact(self):
        contact = self.make_contact(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.delete(f"/api/contacts/{contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PositionTest(BaseTestCase):
    def test_list_positions(self):
        self.APIClient.force_authenticate(user=self.admin_user)

        count = random.randint(1, 10)
        for _ in range(count):
            self.make_position()
        response = self.APIClient.get("/api/positions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_position(self):
        self.APIClient.force_authenticate(user=self.admin_user)

        position = self.make_position()
        response = self.APIClient.get(f"/api/positions/{position.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["id"], position.id)

    def test_update_position(self):
        self.APIClient.force_authenticate(user=self.admin_user)

        position = self.make_position()
        new_name = "ipsum"
        response = self.APIClient.patch(
            f"/api/positions/{position.id}/",
            {
                "name": new_name,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)
        self.assertEqual(response.data["name"], new_name)

    def test_destroy_position(self):
        self.APIClient.force_authenticate(user=self.admin_user)

        position = self.make_position()
        response = self.APIClient.delete(f"/api/positions/{position.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], PositionViewSet)

    def test_forbidden_basic_user_destroy_position(self):
        position = self.make_position()
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.delete(f"/api/positions/{position.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryTest(BaseTestCase):
    def test_list_categories(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_category()
        response = self.APIClient.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["count"], count)

    def test_retrieve_category(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        category = self.make_category()
        response = self.APIClient.get("/api/categories/{}/".format(category.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["id"], category.id)

    def test_create_category(self):
        self.APIClient.force_authenticate(user=self.basic_user)

        category_obj = {
            "name": "ipsum",
        }
        response = self.APIClient.post("/api/categories/", category_obj, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["name"], category_obj["name"].upper())

    def test_update_category(self):
        self.APIClient.force_authenticate(user=self.basic_user)

        category = self.make_category()
        new_name = "ipsum"
        response = self.APIClient.patch(
            "/api/categories/{}/".format(category.id),
            {
                "name": new_name,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)
        self.assertEqual(response.data["name"], new_name.upper())

    def test_admin_user_destroy_category(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        category = self.make_category()
        response = self.APIClient.delete("/api/categories/{}/".format(category.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)

    def test_basic_user_forbidden_destroy_category(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        category = self.make_category()
        response = self.APIClient.delete("/api/categories/{}/".format(category.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(response.renderer_context["view"], CategoryViewSet)

    def test_basic_user_forbidden_destroy_category(self):
        category = self.make_category()
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.delete("/api/categories/{}/".format(category.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

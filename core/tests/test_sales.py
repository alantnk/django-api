import random
from rest_framework.test import force_authenticate
from rest_framework import status
from .base import BaseTestCase
from core.views import SaleViewSet, SaleHistoryViewSet


class SaleTest(BaseTestCase):
    def test_list_sales_by_user(self):
        count = random.randint(1, 10)
        for _ in range(count):
            self.make_sale(user=self.basic_user)
        self.make_sale(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.get("/api/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)
        self.assertEqual(response.data["count"], count)

    def test_status_unauthorized(self):
        response = self.APIClient.get("/api/sales/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_sales_by_admin_user(self):
        for _ in range(5):
            self.make_sale(user=self.basic_user)
        self.make_sale(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.get("/api/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)
        self.assertEqual(response.data["count"], 6)

    def test_retrieve_sale(self):
        sale = self.make_sale(user=self.basic_user)
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.get(f"/api/sales/{sale.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)
        self.assertEqual(response.data["id"], sale.id)

    def test_create_sale(self):
        sale_obj = {**self.sale_post_obj, "client": self.make_client().id}
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.post(
            "/api/sales/",
            sale_obj,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)

        self.assertEqual(response.data["funnel_stage"], sale_obj["funnel_stage"])

    def test_update_sale(self):
        sale = self.make_sale(user=self.basic_user)
        new_status = "done"
        self.APIClient.force_authenticate(user=self.basic_user)
        response = self.APIClient.patch(
            f"/api/sales/{sale.id}/",
            {
                "status": new_status,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)

        self.assertEqual(response.data["id"], sale.id)
        self.assertEqual(response.data["status"], new_status)

    def test_destroy_sale(self):
        sale = self.make_sale(user=self.admin_user)
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.delete(f"/api/sales/{sale.id}/")
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)

    def test_list_sales_by_user_username(self):
        for i in range(10):
            if i == 0:
                self.make_sale(user=self.admin_user)
            else:
                self.make_sale(user=self.basic_user)
        req = self.factory.get(f"/api/sales?search={self.basic_user.username}")
        force_authenticate(req, user=self.admin_user)
        response = SaleViewSet.as_view({"get": "list"})(req)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 9)

    def test_not_update_sale_by_another_user(self):
        sale = self.make_sale(user=self.basic_user)
        new_status = "on_hold"
        self.APIClient.force_authenticate(user=self.admin_user)
        response = self.APIClient.patch(
            f"/api/sales/{sale.id}/",
            {
                "status": new_status,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(response.renderer_context["view"], SaleViewSet)

    def test_not_update_sale_closed(self):
        self.APIClient.force_authenticate(user=self.basic_user)
        sale = self.make_sale(user=self.basic_user, closed=True)
        new_data = "lorem ipsum sit amet"
        resp = self.APIClient.patch(
            f"/api/sales/{sale.id}/",
            {
                "funnel_stage": new_data,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp.renderer_context["view"], SaleViewSet)


class SaleHistoryTest(BaseTestCase):
    def test_list_sale_history(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        obj = {"funnel_stage": "lorem ipsum", "status": "on_hold", "chance": 99}
        sale = self.make_sale(user=self.admin_user)
        self.APIClient.patch(
            f"/api/sales/{sale.id}/",
            obj,
            format="json",
        )

        resp = self.APIClient.get("/api/sales-history/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["count"], 3)

    def test_status_unauthorized(self):
        resp = self.APIClient.get("/api/sales-history/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(resp.renderer_context["view"], SaleHistoryViewSet)

    def test_post_method_not_allowed(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        resp_post = self.APIClient.post("/api/sales-history/")
        self.assertEqual(resp_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIsInstance(resp_post.renderer_context["view"], SaleHistoryViewSet)

    def test_patch_method_not_allowed(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        resp_patch = self.APIClient.patch("/api/sales-history/1/")
        self.assertEqual(resp_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIsInstance(resp_patch.renderer_context["view"], SaleHistoryViewSet)

    def test_delete_method_not_allowed(self):
        self.APIClient.force_authenticate(user=self.admin_user)
        resp_delete = self.APIClient.delete("/api/sales-history/1/")
        self.assertEqual(resp_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIsInstance(resp_delete.renderer_context["view"], SaleHistoryViewSet)

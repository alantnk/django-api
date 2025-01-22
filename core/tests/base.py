from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from model_bakery import baker
import datetime

# from core.models import Client, Category, Position


class BaseTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.APIClient = APIClient()
        self.super_user = baker.make("auth.User")
        self.simple_user = baker.make("auth.User", is_staff=False, is_superuser=False)
        self.staff_user = baker.make("auth.User", is_staff=True)
        self.client_post_obj = {
            "fantasy_name": "spam eggs x1",
            "office_name": "spam eggs xy",
            "phone": "8899445568014",
            "location": "Land",
            "state_code": "44",
            "zip_code": "OXOXOXOX",
            "district": "Alambra",
            "idoc": "x17360284p2z58",
            "email": "matrix@example.com",
        }
        self.sale_post_obj = {
            "estimated_value": 90.4,
            "chance": 100,
            "funnel_stage": "lorem ipsum",
            "expected_date": datetime.datetime.now(),
        }

        return super().setUp()

    def make_position(self, **kwargs):
        position = baker.make("core.Position", _refresh_after_create=True, **kwargs)
        return position

    def make_category(self, **kwargs):
        category = baker.make("core.Category", _refresh_after_create=True, **kwargs)
        return category

    def make_client(self, **kwargs):
        client = baker.make("core.Client", _refresh_after_create=True, **kwargs)
        return client

    def make_contact(self, **kwargs):
        contact = baker.make("core.Contact", _refresh_after_create=True, **kwargs)
        return contact

    def make_sale(self, **kwargs):
        sale = baker.make("core.Sale", _refresh_after_create=True, **kwargs)
        return sale

    def make_task(self, **kwargs):
        task = baker.make("core.Task", _refresh_after_create=True, **kwargs)
        return task

    def make_tag(self, **kwargs):
        tag = baker.make("core.Tag", _refresh_after_create=True, **kwargs)
        return tag

    def make_position(self, **kwargs):
        position = baker.make("core.Position", _refresh_after_create=True, **kwargs)
        return position

    def make_category(self, **kwargs):
        category = baker.make("core.Category", _refresh_after_create=True, **kwargs)
        return category

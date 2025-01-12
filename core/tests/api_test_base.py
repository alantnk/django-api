import time
from rest_framework.test import APITestCase, APIRequestFactory

from model_bakery import baker

# from core.models import Client, Category, Position


class APITestBase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make("auth.User")
        self.client_post_obj = {
            "fantasy_name": "spam eggs x1",
            "office_name": "spam eggs xy",
            "phone": "8899445568014",
            "location": "Land",
            "state_code": "44",
            "zip_code": "OXOXOXOX",
            "district": "Alambra",
            "idoc": "x17360284p2z58",
            "email": "laYwdjmxGj@example.com",
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

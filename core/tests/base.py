from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from model_bakery import baker
import datetime

from .utils import (
    make_category,
    make_contact,
    make_client,
    make_position,
    make_tag,
    make_task,
    make_sale,
)

User = get_user_model()


class BaseTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.APIClient = APIClient()
        self.super_user = baker.make(User)
        self.simple_user = baker.make(User, is_staff=False, is_superuser=False)
        self.staff_user = baker.make(User, is_staff=True)
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
        position = make_position(**kwargs)
        return position

    def make_category(self, **kwargs):
        category = make_category(**kwargs)
        return category

    def make_client(self, **kwargs):
        client = make_client(**kwargs)
        return client

    def make_contact(self, **kwargs):
        contact = make_contact(**kwargs)
        return contact

    def make_sale(self, **kwargs):
        sale = make_sale(**kwargs)
        return sale

    def make_task(self, **kwargs):
        task = make_task(**kwargs)
        return task

    def make_tag(self, **kwargs):
        tag = make_tag(**kwargs)
        return tag

    def make_position(self, **kwargs):
        position = make_position(**kwargs)
        return position

    def make_category(self, **kwargs):
        category = make_category(**kwargs)
        return category

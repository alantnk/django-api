import random
from model_bakery import baker

from core.models import Client, Category, Position
import time


def make_position(i: int = 1):
    position = baker.make(
        "core.Position",
        name=f"Position {i}",
    )
    return position


def make_category(i: int = 1):
    category = baker.make(
        "core.Category",
        name=f"Category {i}",
    )
    return category


def make_client(i=1):
    client = baker.make(
        "core.Client",
        fantasy_name=f"Spam Eggs {i}",
        office_name=f"Spam Eggs {i}",
        idoc=f"x{round(time.time() * 1000)}",
        category=random.choice(Category.objects.all()),
    )
    return client


def make_contact(i: int = 1):
    contact = baker.make(
        "core.Contact",
        full_name=f"John Doe {i}",
        email=f"john.doe{i}@example.com",
        client=random.choice(Client.objects.all()),
        position=random.choice(Position.objects.all()),
    )
    return contact


def make_data():
    for i in range(4):
        make_category(i + 1)
        make_position(i + 1)
    print("Categories & Positions CREATED")

    for i in range(50):
        make_client(i + 1)
    print("Clients CREATED")

    for i in range(120):
        make_contact(i + 1)
    print("Contacts CREATED")

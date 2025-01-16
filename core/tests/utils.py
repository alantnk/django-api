import random
from model_bakery import baker

from core.models import Client, Category, Position
import time


def get_random_email():
    id = random.randint(1000, 9999)
    name = random.choice(["abc", "xyz", "kvm", "pgv", "qwe"])
    domain = random.choice(["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"])
    return f"{name}{id}@{domain}"


def get_random_full_name():
    first_name = random.choice(
        [
            "John",
            "Jane",
            "Bob",
            "Alice",
            "Michael",
            "Jessica",
            "David",
            "Sarah",
            "William",
            "Emily",
        ]
    )
    last_name = random.choice(
        [
            "Doe",
            "Smith",
            "Brown",
            "King",
            "Davis",
            "Garcia",
            "Rodriguez",
            "Martinez",
            "Costa",
        ]
    )
    return f"{first_name} {last_name}"


def get_random_decimal():
    num = random.randint(10, 99)
    return num


def make_position():
    position = baker.make(
        "core.Position",
        name=f"Position {get_random_decimal()}",
    )
    return position


def make_category():
    category = baker.make(
        "core.Category",
        name=f"Category {get_random_decimal()}",
    )
    return category


def make_client(**kwargs):
    name = f"Spam Eggs {get_random_decimal()}"
    client = baker.make(
        "core.Client",
        fantasy_name=name,
        office_name=name,
        idoc=f"x{round(time.time() * 1000)}",
        category=random.choice(Category.objects.all()),
        **kwargs,
    )
    return client


def make_contact(**kwargs):
    contact = baker.make(
        "core.Contact",
        full_name=get_random_full_name(),
        email=get_random_email(),
        client=random.choice(Client.objects.all()),
        position=random.choice(Position.objects.all()),
        **kwargs,
    )
    return contact


def make_data(user):
    for i in range(4):
        make_category()
        make_position()
    print("Categories & Positions CREATED")

    for i in range(50):
        make_client(user=user)
    print("Clients CREATED")

    for i in range(120):
        make_contact(user=user)
    print("Contacts CREATED")

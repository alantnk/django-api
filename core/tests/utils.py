import datetime
from faker import Faker
from django.contrib.auth import get_user_model
from model_bakery import baker
from core.models import Category, Client, Position, Tag

fake = Faker(["es_ES", "it_IT"])
Faker.seed(1998)

User = get_user_model()


def make_tag(**kwargs):
    tag = baker.make("core.Tag", _refresh_after_create=True, **kwargs)
    return tag


def make_position(**kwargs):
    position = baker.make("core.Position", _refresh_after_create=True, **kwargs)
    return position


def make_category(**kwargs):
    category = baker.make("core.Category", _refresh_after_create=True, **kwargs)
    return category


def make_task(**kwargs):
    task = baker.make("core.Task", _refresh_after_create=True, **kwargs)
    return task


def make_sale(**kwargs):
    sale = baker.make("core.Sale", _refresh_after_create=True, **kwargs)
    return sale


def make_client(**kwargs):

    client = baker.make(
        "core.Client",
        _refresh_after_create=True,
        **kwargs,
    )
    return client


def make_contact(**kwargs):
    contact = baker.make(
        "core.Contact",
        _refresh_after_create=True,
        **kwargs,
    )
    return contact


def get_random_instance(model):
    return model.objects.order_by("?").first()


def get_admin_user():
    return User.objects.filter(is_staff=True).first()


def make_data():
    for i in range(4):
        make_category(name=fake.safe_color_name())
        make_position(name=fake.job())
        make_tag(name=fake.currency_code())
    print("Categories,Positions,Tags CREATED")

    for i in range(2):
        names = ["kelly", "smith"]
        user = User.objects.create_user(
            username=names[i],
            email=f"{names[i]}@abc.com",
            password="qwerty",
        )
        user.is_staff = True if i > 0 else False
        user.save()
    print("Users CREATED")

    for i in range(50):
        fake_com_name = fake.company()
        make_client(
            user=get_random_instance(User),
            fantasy_name=fake_com_name,
            office_name=fake_com_name,
            idoc=f"X{fake.msisdn()}",
            phone=fake.ssn(),
            category=get_random_instance(Category),
            location=fake.city(),
            state_code=fake.random_number(digits=2, fix_len=True),
            zip_code=fake.postcode(),
            district=fake.street_suffix(),
            address=fake.address(),
        )
    print("Clients CREATED")

    for i in range(120):
        make_contact(
            user=get_random_instance(User),
            client=get_random_instance(Client),
            full_name=fake.name(),
            email=fake.free_email(),
            phone=fake.ssn(),
            district=fake.word(),
            address=fake.address(),
            position=get_random_instance(Position),
        )
    print("Contacts CREATED")

    for i in range(10):
        make_sale(
            user=get_random_instance(User),
            client=get_random_instance(Client),
            chance=fake.random_int(min=1, max=100),
            status=fake.word(ext_word_list=["in_progress", "on_hold", "pending"]),
            funnel_stage=fake.sentence(),
            expected_date=fake.future_datetime(tzinfo=datetime.timezone.utc),
        )
    print("Sales CREATED")

    make_task(
        user=get_random_instance(User),
        tags=[get_random_instance(Tag), get_random_instance(Tag)],
        title=fake.word(ext_word_list=["pop", "boom", "knock", "crack"]),
        description=fake.catch_phrase(),
        due_date=fake.date_time(tzinfo=datetime.timezone.utc),
        status="todo",
        closed=False,
    )
    print("Tasks CREATED")

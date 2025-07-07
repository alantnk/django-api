# CRM in Django

This project aims to build a simple CRM using Django.

## Installation and Usage

#### 1. Clone the repository

```bash
$ git clone git@github.com:alantnk/django-api.git
$ cd django-api
```

#### 2. Virtual environment

Create and activate the environment:

```bash
$ virtualenv .venv
$ source .venv/bin/activate
```

**See:** [**How to install virtualenv on Linux and Windows**](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

#### 3. Installation

Run the packages installation:

```bash
$ pip install -r requirements.txt
```

#### 4. Migrations

Rename the `.env-example` file to `.env` and run the migrations:

```bash
$ python3 manage.py migrate
```

#### 5. Start server

First, create a user with the command `python3 manage.py createsuperuser`.

Fill in the fields and then start the server:

```bash
$ python3 manage.py runserver
```

Access the base address http://127.0.0.1:8000 and read the documentation.

#### 6. Seeds (Optional)

To pre-populate the database, open the Django **shell** with `python3 manage.py shell`

```py
from core.tests import make_data
make_data()
```

Then close the terminal and run the server again.

## Tests

```bash
$ python3 manage.py test
```

Or run `pytest`.

#### HTTP Client(Insomnia)

If you use Insomnia, import the **api_collection.json** file.

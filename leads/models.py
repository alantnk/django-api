from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(BaseModel):
    fantasy_name = models.CharField(max_length=100)
    office_name = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.fantasy_name


class Contact(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

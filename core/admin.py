from django.contrib import admin

from core.models import Client, Category, Contact, Position


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["fantasy_name", "office_name", "idoc", "email"]
    list_display = ["fantasy_name", "office_name", "idoc", "email"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "email"]
    list_display = ["first_name", "last_name", "email", "position"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

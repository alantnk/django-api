from django.contrib import admin

from core.models import Client, Category, Contact, Position, Sale, Task, Tag


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["fantasy_name", "office_name", "idoc", "email"]
    list_display = ["fantasy_name", "office_name", "idoc", "email"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "created_at", "updated_at"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ["full_name", "email"]
    list_display = ["full_name", "email", "client", "position"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "created_at", "updated_at"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    search_fields = ["client"]
    list_display = ["client", "created_at", "updated_at"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "user", "status", "due_date"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

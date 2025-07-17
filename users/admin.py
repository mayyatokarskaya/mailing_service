from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("avatar", "phone_number", "country")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("avatar", "phone_number", "country")}),)

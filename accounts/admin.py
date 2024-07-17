from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Supervisor, Owner, Driver
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):

    list_display = [
        "user", "fleet",
    ]

    raw_id_fields = ['user']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]
    raw_id_fields = ['user']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]
    raw_id_fields = ['user']




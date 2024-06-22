from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OurBookUser


@admin.register(OurBookUser)
class OurBookAdmin(admin.ModelAdmin):
    list_display = ("cpf",)

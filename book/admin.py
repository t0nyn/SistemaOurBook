from django.contrib import admin
from . import models
from django.utils.html import format_html


# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "category", "format_image")

    def format_image(self, obj):
        return format_html(f'<img src="{obj.cover.url}">')

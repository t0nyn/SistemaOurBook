from django.contrib import admin
from . import models
from django.utils.html import format_html


# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "category", "image_url")

    def image_url(self, obj):
        return format_html(f'<a href="{obj.cover.url}">link</a>')
        # return f'<a href="{obj.cover.url}"></a>'

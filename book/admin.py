from django.contrib import admin
from . import models
from django.utils.html import format_html


# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "imagem")

    def imagem(self, obj):
        return format_html(f'<a href="{obj.cover.url}">link</a>')

    def format_categories(self, obj):
        return ", ".join([category.name for category in obj.categories])

    def titulo(self, obj):
        return obj.name

    def autor(self, obj):
        return obj.author

    # format_categories.short_description("Categories")


@admin.register(models.BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo")

    def titulo(self, obj):
        return obj.book.name

    def codigo(self, obj):
        return obj.id

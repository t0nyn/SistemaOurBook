from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="static/images/books")
    description = models.CharField(max_length=2000)
    edition = models.IntegerField()
    year = models.IntegerField()
    num_pages = models.IntegerField()


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    all_status = [
        ("AVAILABLE", "Available"),
        ("BORROWED", "Borrowed"),
        ("RESERVED", "Reserved"),
    ]
    current_status = models.CharField(
        max_length=15, choices=all_status, default="AVAIABLE"
    )

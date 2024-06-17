from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="static/images/books")
    description = models.CharField(max_length=2000, null=True)
    edition = models.CharField(max_length=100)
    year = models.IntegerField()
    num_pages = models.IntegerField()

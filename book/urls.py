from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("book/<int:id>", views.book_page, name="book_page"),
]

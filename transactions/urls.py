from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from . import views

urlpatterns = [
    path("loans", views.loans, name="loans"),
    path("loan/<int:id>/", views.loan_item, name="loan_item"),
    path("add_loan", views.add_loan, name="add_loan"),
    path("return_book", views.return_book, name="return_book"),
    path("add_renovation", views.add_renovation, name="add_renovation"),
]

from django.shortcuts import render
from django.shortcuts import render, resolve_url, redirect
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from book.models import Book, Category
from transactions.models import Loan
from django.contrib.auth.models import User


# Create your views here.
@login_required
def home(request):
    if request.user.is_superuser:
        loans = Loan.objects.all()
        context = {
            "loans": loans,
        }
        return render(request, "adm/adm.html", context=context)

    books = Book.objects.all()[:8]
    categories = Category.objects.all()
    context = {
        "books": books,
        "username": request.user,
        "categories": categories,
    }
    return render(request, "home/home.html", context=context)


def book_page(request, id):
    book = Book.objects.get(id=id)
    same_category_books = Book.objects.exclude(id=id).filter(category=book.category)
    context = {
        "book": book,
        "username": request.user,
        "same_category_books": same_category_books,
    }
    return render(request, "book/book.html", context=context)


# def category_page(request, category):
#     return render()

from django.shortcuts import render
from django.shortcuts import render, resolve_url, redirect
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.contrib.auth.models import User


# Create your views here.
@login_required
def home(request):
    books = Book.objects.all()[:8]
    context = {"books": books, "username": request.user}
    return render(request, "home/home.html", context=context)


def book_page(request, id):
    book = Book.objects.get(id=id)
    context = {"book": book, "username": request.user}
    return render(request, "book/book.html", context=context)

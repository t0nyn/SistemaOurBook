from django.shortcuts import render, resolve_url, redirect
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from user.models import OurBookUser
from book.models import Book


# Create your views here.
def register(request):
    context = {"login_url": resolve_url("login")}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        cpf = request.POST.get("cpf")
        user = OurBookUser.objects.create_user(
            username=username, password=password, cpf=cpf
        )
        login_user(request, user)
        next_url = request.GET.get("next", "home")
        return redirect(resolve_url("home"))

    return render(request, "user/register.html", context=context)


def login(request):
    context = {"login_fail": None}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(resolve_url(next_url))

        context["login_fail"] = True

    return render(request, "user/login.html", context=context)

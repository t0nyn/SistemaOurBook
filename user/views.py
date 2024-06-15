from django.shortcuts import render, resolve_url, redirect
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def register(request):
    return HttpResponse('hello')

@login_required
def home(request):
    return HttpResponse('home')

def login(request):
    context = {
        'register_url' : resolve_url('register'),
        'login_fail' : None
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(resolve_url(next_url))
    
        context['login_fail'] = True
    
    return render(request, 'user/login.html', context=context)
   

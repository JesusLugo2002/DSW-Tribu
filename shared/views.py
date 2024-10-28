from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if (user := authenticate(request, username=username, password=password)):
                login(request, user)
                return redirect('echos:echos-list')
    else:
        form = LoginForm()
    return render(request, 'login.html', dict(form=form))

def user_signup(request):
    form = SignupForm(request.POST or None)
    return render(request, 'signup.html', dict(form=form))

def user_logout(request):
    logout(request)
    return redirect('login')
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm

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
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'signup.html')
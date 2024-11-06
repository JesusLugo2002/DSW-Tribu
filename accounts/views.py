from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


# Create your views here.
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect('echos:echo-list')
    return render(request, 'login.html', dict(form=form))


def user_signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('echos:echo-list')
    return render(request, 'signup.html', dict(form=form))


def user_logout(request):
    logout(request)
    return redirect('login')

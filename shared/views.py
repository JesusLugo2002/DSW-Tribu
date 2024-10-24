from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    return render(request, 'login.html')
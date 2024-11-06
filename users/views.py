from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
def user_list(request):
    pass


def user_detail(request, username):
    other_user = User.objects.get(username=username)
    return render(request, 'users/detail.html', dict(other_user=other_user))


def user_echos(request, user_pk):
    pass


def my_user(request):
    pass


def user_edit(request, user_pk):
    pass

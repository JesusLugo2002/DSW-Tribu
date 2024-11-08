from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


@login_required
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/list.html', dict(users=users))


@login_required
def user_detail(request, username):
    other_user = User.objects.get(username=username)
    echos = other_user.echos.all()
    return render(
        request,
        'users/user/detail.html',
        dict(other_user=other_user, echos=echos[:5], echos_quantity=echos.count()),
    )


@login_required
def user_echos(request, username):
    other_user = User.objects.get(username=username)
    echos = other_user.echos.all()
    return render(request, 'users/user/echos.html', dict(other_user=other_user, echos=echos))


@login_required
def my_user(request):
    return redirect('users:user-detail', username=request.user)


@login_required
def user_edit(request, username):
    pass

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden, HttpResponse

from .models import Profile
from .forms import EditProfileForm


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
    if request.user.username != username:
        return HttpResponseForbidden("You can not edit another user profile!")
    user_profile = Profile.objects.get(user=request.user)
    form = EditProfileForm(request.POST or None, instance=user_profile)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect('users:my-user')
    return render(request, "users/user/edit.html", dict(form=form))

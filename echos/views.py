from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AddEchoForm
from .models import Echo


# Create your views here.
@login_required
def echos_list(request):
    echos = Echo.objects.all()
    return render(request, 'echos/list.html', dict(echos=echos))


@login_required
def echo_add(request):
    form = AddEchoForm(request.POST or None)
    if form.is_valid():
        echo = form.save(commit=False)
        echo.user = request.user
        echo.save()
        return redirect('echos:echo-list')
    return render(request, 'echos/add.html', dict(form=form))


@login_required
def echo_detail(request, echo_pk):
    echo = Echo.objects.get(pk=echo_pk)
    waves = echo.waves.all()
    last_waves = waves[:5]
    waves_quantity = len(waves)
    return render(
        request,
        'echos/echo/detail.html',
        dict(echo=echo, waves=last_waves, waves_quantity=waves_quantity),
    )


@login_required
def echo_waves(request, echo_pk):
    echo = Echo.objects.get(pk=echo_pk)
    waves = echo.waves.all()
    return render(
        request,
        'echos/echo/waves.html',
        dict(echo=echo, waves=waves),
    )


def echo_edit(request, echo_pk):
    return HttpResponse('Work in progress')


def echo_delete(request, echo_pk):
    return HttpResponse('Work in progress')


def echo_wave_add(request, echo_pk):
    return HttpResponse('Work in progress')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from shared.utils import assert_owner_of

from waves.forms import AddWaveForm

from .forms import AddEchoForm, EditEchoForm
from .models import Echo


@login_required
def echos_list(request: HttpRequest) -> HttpResponse:
    echos = Echo.objects.all()
    return render(request, 'echos/list.html', dict(echos=echos))


@login_required
def echo_add(request: HttpRequest) -> HttpResponse:
    form = AddEchoForm(request.user, request.POST or None)
    if form.is_valid():
        echo = form.save()
        return redirect(echo)
    return render(request, 'echos/add.html', dict(form=form))


@login_required
def echo_detail(request: HttpRequest, echo_pk: int) -> HttpResponse:
    echo = Echo.objects.get(pk=echo_pk)
    waves = echo.waves.all()
    return render(
        request,
        'echos/echo/detail.html',
        dict(echo=echo, waves=waves[:5], waves_quantity=len(waves)),
    )


@login_required
def echo_waves(request: HttpRequest, echo_pk: int) -> HttpResponse:
    echo = Echo.objects.get(pk=echo_pk)
    waves = echo.waves.all()
    return render(
        request,
        'echos/echo/waves.html',
        dict(echo=echo, waves=waves),
    )


@login_required
@assert_owner_of('echo')
def echo_edit(request: HttpRequest, echo_pk: int) -> HttpResponse | HttpResponseForbidden:
    echo = Echo.objects.get(pk=echo_pk)
    form = EditEchoForm(request.POST or None, instance=echo)
    if form.is_valid():
        echo = form.save()
        return redirect(echo)
    return render(request, 'echos/echo/edit.html', dict(form=form))


@login_required
@assert_owner_of('echo')
def echo_delete(request: HttpRequest, echo_pk: int) -> HttpResponse | HttpResponseForbidden:
    echo = Echo.objects.get(pk=echo_pk)
    echo.delete()
    return redirect('echos:echo-list')


@login_required
def echo_wave_add(request: HttpRequest, echo_pk: int) -> HttpResponse:
    echo = Echo.objects.get(pk=echo_pk)
    form = AddWaveForm(request.user, echo, request.POST or None)
    if form.is_valid():
        wave = form.save()
        return redirect(echo)
    return render(request, 'echos/echo/add-wave.html', dict(form=form))

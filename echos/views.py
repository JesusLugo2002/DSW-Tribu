from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from shared.utils import assert_owner_of

from waves.forms import AddWaveForm

from .forms import AddEchoForm, EditEchoForm
from .models import Echo


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
    return render(
        request,
        'echos/echo/detail.html',
        dict(echo=echo, waves=waves[:5], waves_quantity=len(waves)),
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


@login_required
@assert_owner_of('echo')
def echo_edit(request, echo_pk):
    echo = Echo.objects.get(pk=echo_pk)
    form = EditEchoForm(request.POST or None, instance=echo)
    if form.is_valid():
        echo = form.save()
        return redirect('echos:echo-list')
    return render(request, 'echos/echo/edit.html', dict(form=form))


@login_required
@assert_owner_of('echo')
def echo_delete(request, echo_pk):
    echo = Echo.objects.get(pk=echo_pk)
    echo.delete()
    return redirect('echos:echo-list')


@login_required
def echo_wave_add(request, echo_pk):
    form = AddWaveForm(request.POST or None)
    echo = Echo.objects.get(pk=echo_pk)
    if form.is_valid():
        wave = form.save(commit=False)
        wave.user = request.user
        wave.echo = echo
        wave.save()
        return redirect('echos:echo-list')
    return render(request, 'echos/echo/add-wave.html', dict(form=form))

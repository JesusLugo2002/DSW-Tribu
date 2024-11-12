from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from shared.utils import assert_owner_of
from .forms import EditWaveForm
from .models import Wave

@login_required
@assert_owner_of('wave')
def wave_edit(request: HttpRequest, wave_pk: int) -> HttpResponse | HttpResponseForbidden:
    wave = Wave.objects.get(pk=wave_pk)
    form = EditWaveForm(request.POST or None, instance=wave)
    if form.is_valid():
        wave = form.save()
        return redirect(wave.echo)
    return render(request, 'waves/edit.html', dict(form=form))

@login_required
@assert_owner_of('wave')
def wave_delete(request: HttpRequest, wave_pk: int) -> HttpResponse | HttpResponseForbidden:
    wave = Wave.objects.get(pk=wave_pk)
    echo = wave.echo
    wave.delete()
    return redirect(echo)
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .forms import EditWaveForm
from .models import Wave

@login_required
def wave_edit(request, wave_pk):
    wave = Wave.objects.get(pk=wave_pk)
    if request.user != wave.user:
        return HttpResponseForbidden()
    form = EditWaveForm(request.POST or None, instance=wave)
    if form.is_valid():
        wave = form.save()
        return redirect('echos:echo-list')
    return render(request, 'waves/edit.html', dict(form=form))

@login_required
def wave_delete(request, wave_pk):
    wave = Wave.objects.get(pk=wave_pk)
    if request.user != wave.user:
        return HttpResponseForbidden()
    wave.delete()
    return redirect('echos:echo-list')
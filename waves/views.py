from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shared.utils import assert_owner_of

from .forms import EditWaveForm
from .models import Wave

@login_required
@assert_owner_of('wave')
def wave_edit(request, wave_pk):
    wave = Wave.objects.get(pk=wave_pk)
    form = EditWaveForm(request.POST or None, instance=wave)
    if form.is_valid():
        wave = form.save()
        return redirect('echos:echo-list')
    return render(request, 'waves/edit.html', dict(form=form))

@login_required
@assert_owner_of('wave')
def wave_delete(request, wave_pk):
    wave = Wave.objects.get(pk=wave_pk)
    wave.delete()
    return redirect('echos:echo-list')
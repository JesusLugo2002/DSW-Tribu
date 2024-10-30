from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Echo
from waves.models import Wave

# Create your views here.
@login_required
def echos_list(request):
    echos = Echo.objects.all().order_by('-created_at')
    return render(request, 'echos/list.html', dict(echos=echos))

@login_required
def echo_detail(request, echo_id):
    echo = Echo.objects.get(id=echo_id)
    waves = Wave.objects.filter(echo=echo)
    last_waves = waves.order_by('-created_at')[:5]
    waves_quantity = len(waves)
    return render(request, 'echos/echo/detail.html', dict(echo=echo, waves=last_waves, waves_quantity=waves_quantity))
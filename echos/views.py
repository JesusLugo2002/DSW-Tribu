from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Echo

# Create your views here.
@login_required
def echos_list(request):
    echos = Echo.objects.all().order_by('-created_at')
    return render(request, 'echos/list.html', dict(echos=echos))

@login_required
def echo_detail(request, echo_id):
    echo = Echo.objects.get(id=echo_id)
    return render(request, 'echos/echo/detail.html', dict(echo=echo))
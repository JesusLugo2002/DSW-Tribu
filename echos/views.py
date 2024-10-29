from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Echo

# Create your views here.
@login_required
def echos_list(request):
    echos = Echo.objects.all().order_by('-created_at')
    return render(request, 'echos/echos-list.html', dict(echos=echos))
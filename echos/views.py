from django.shortcuts import render
from .models import Echo
from django.http import HttpResponse

# Create your views here.
def     echos_list(request):
    return render(request, 'echos/echos-list.html')
from django.urls import path
from . import views

app_name = 'echos'

urlpatterns = [
    path('', views.echos_list, name="echos-list")
]

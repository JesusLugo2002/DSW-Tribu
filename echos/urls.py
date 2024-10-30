from django.urls import path
from . import views

app_name = 'echos'

urlpatterns = [
    path('', views.echos_list, name="echos-list"),
    path('<echo_id>/', views.echo_detail, name='echo-detail')
]

# echo/id/: Echo con los últimos 5 waves
# echo/id/waves: Todos los waves del echo
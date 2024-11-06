from django.urls import path

from . import views

app_name = 'echos'

urlpatterns = [
    path('', views.echos_list, name='echo-list'),
    path('<echo_pk>/', views.echo_detail, name='echo-detail'),
    path('<echo_pk>/waves/', views.echo_waves, name='echo-waves'),
    path('<echo_pk>/edit/', views.echo_edit, name='echo-edit'),
    path('<echo_pk>/delete/', views.echo_delete, name='echo-delete'),
    path('<echo_pk>/waves/add', views.echo_wave_add, name='echo-wave-add'),
]

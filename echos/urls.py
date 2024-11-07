from django.urls import path

from . import views

app_name = 'echos'

urlpatterns = [
    path('', views.echos_list, name='echo-list'),
    path('add/', views.echo_add, name='echo-add'),
    path('<int:echo_pk>/', views.echo_detail, name='echo-detail'),
    path('<int:echo_pk>/waves/', views.echo_waves, name='echo-waves'),
    path('<int:echo_pk>/edit/', views.echo_edit, name='echo-edit'),
    path('<int:echo_pk>/delete/', views.echo_delete, name='echo-delete'),
    path('<int:echo_pk>/waves/add/', views.echo_wave_add, name='echo-wave-add'),
]

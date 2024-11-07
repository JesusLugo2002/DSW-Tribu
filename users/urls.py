from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('@me/', views.my_user, name='my-user'),
    path('@me/edit/', views.user_edit, name='user-edit'),
    path('<str:username>/', views.user_detail, name='user-detail'),
    path('<str:username>/echos/', views.user_echos, name='user-echos'),
]

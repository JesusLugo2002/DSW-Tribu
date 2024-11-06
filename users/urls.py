from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('<username>/', views.user_detail, name='user-detail'),
    path('<username>/echos/', views.user_echos, name='user-echos'),
    path('@me/', views.my_user, name='my-user'),
    path('@me/edit/', views.user_edit, name='user-edit'),
]

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('<user_pk>/', views.user_detail, name='user-detail'),
    path('<user_pk>/echos/', views.user_echos, name='user-echos')
]

# path('@me/', redirect()) ???

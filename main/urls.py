"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import accounts.views

urlpatterns = [
    path('', lambda r: redirect('echos:echo-list')),
    path('admin/', admin.site.urls),
    path('login/', accounts.views.user_login, name='login'),
    path('signup/', accounts.views.user_signup, name='signup'),
    path('logout/', accounts.views.user_logout, name='logout'),
    path('echos/', include('echos.urls')),
    path('waves/', include('waves.urls')),
    path('users/', include('users.urls'))
]

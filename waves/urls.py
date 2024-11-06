from django.urls import path
from . import views

app_name = 'waves'

urlpatterns = [
   path('<wave_pk>/edit/', views.wave_edit, name='wave-edit'),
   path('<wave_pk>/delete/', views.wave_delete, name='wave-delete')
]

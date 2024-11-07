from django.urls import path
from . import views

app_name = 'waves'

urlpatterns = [
   path('<int:wave_pk>/edit/', views.wave_edit, name='wave-edit'),
   path('<int:wave_pk>/delete/', views.wave_delete, name='wave-delete')
]

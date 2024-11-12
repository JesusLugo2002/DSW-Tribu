from django.contrib import admin
from .models import Wave

# Register your models here.
@admin.register(Wave)
class WaveAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'echo', 'created_at', 'updated_at']
    ordering = ['pk']
from django.contrib import admin
from .models import Echo

# Register your models here.
@admin.register(Echo)
class EchoAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "created_at", "updated_at"]
    ordering = ['pk']
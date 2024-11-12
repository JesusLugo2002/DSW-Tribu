from django.conf import settings
from django.db import models


# Create your models here.
class Wave(models.Model):
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    echo = models.ForeignKey('echos.Echo', related_name='waves', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Wave #{self.pk} by {self.user} linked to Echo #{self.echo.pk}'

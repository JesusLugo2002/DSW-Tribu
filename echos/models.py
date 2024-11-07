from django.conf import settings
from django.db import models


# Create your models here.
class Echo(models.Model):
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='echos')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Echo #{self.id} by {self.user}'

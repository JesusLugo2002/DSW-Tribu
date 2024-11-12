from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
    )
    avatar = models.ImageField(
        blank=True, 
        null=True, 
        upload_to='avatars', 
        default='avatars/noavatar.png'
    )
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['user']
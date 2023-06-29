from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=100, **NULLABLE)
    token = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32)
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

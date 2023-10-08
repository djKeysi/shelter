from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from dogs.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True,verbose_name='почта')
    phone = models.CharField(max_length=35,verbose_name='номер телефона',**NULLABLE)
    telegram = models.CharField(max_length=35, verbose_name='Telegram username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/',verbose_name='аватар', **NULLABLE)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


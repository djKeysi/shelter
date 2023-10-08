from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='порода')
    discription = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'порода'
        verbose_name_plural = 'породы'


class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='кличка собаки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='порода')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='фотография')
    birth_day = models.DateField(**NULLABLE, verbose_name='дата рождения')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.name} {self.category}'

    class Meta:
        verbose_name = 'собака'
        verbose_name_plural = 'собаки'


class Parent(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='кличка собаки')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='порода')
    birth_day = models.DateField(**NULLABLE, verbose_name='дата рождения')


    def __str__(self):
        return f'{self.name} {self.category}'


    class Meta:
        verbose_name = 'предок'
        verbose_name_plural = 'предки'

# Create your models here.

from django.apps import AppConfig


class DogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dogs'
    verbose_name = 'Собаки'

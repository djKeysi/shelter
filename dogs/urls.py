from django.urls import path

from dogs.apps import DogConfig
from dogs.views import index, categories,category_dogs

app_name = DogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('<int:pk>/dogs/', category_dogs, name='category_dogs'),

]

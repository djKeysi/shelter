from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from dogs.apps import DogConfig
from dogs.views import IndexView, CategoryListView, DogListView, DogCreateView, DogUpdateView, DogDeleteView

app_name = DogConfig.name

urlpatterns = [
    path('',cache_page(60)(IndexView.as_view()), name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/dogs/', DogListView.as_view(), name='category_dogs'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/update/<int:pk>', DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>',never_cache(DogDeleteView.as_view()), name='dog_delete'),

]

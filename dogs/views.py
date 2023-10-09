from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from dogs.forms import DogForm, ParentForm
from dogs.models import Category, Dog, Parent
from dogs.services import get_categories_cache


# def index(request):
#     context = {
#         'object_list': Category.objects.all()[:3],
#         'title': 'Питомник - Главная',
#     }
#     return render(request, 'dogs/index.html', context)





class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - Главная'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data


# def categories(request):
#     context = {
#         'object_list': Category.objects.all(),
#         'title': 'Питомник - все наши породы',
#     }
#     return render(request, 'dogs/categories.html',context)

class CategoryListView(LoginRequiredMixin,ListView):
    model = Category



    extra_context = {
        'title': 'Питомник - все наши породы',
        'object_list': get_categories_cache()
        # 'object_list': Dog.objects.filter(category_id=pk,
        # owner=request.user)
    }

    def get_object(self):
        #queryset = super().get_queryset()
        #queryset =queryset.filter(category_id=self.kwargs.get("pk"), owner=self.queryset.user)

        #queryset = queryset.filter(category_id=self.kwargs.get("pk"), owner=queryset.user)
       # return queryset
        return self.queryset.user


# def category_dogs(request,pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Dog.objects.filter(category_id=pk,owner=request.user),
#         'title': f'Собаки породы  - все наши породы {category_item.name}',
#         'category_pk': category_item.pk,
#     }
#     return render(request, 'dogs/dogs_list.html',context)

class DogListView(LoginRequiredMixin,ListView):
    model = Dog

    def get_queryset(self):
        queryset= super().get_queryset().filter(category_id=self.kwargs.get("pk"),)
        # queryset = super().get_queryset()
        # queryset = queryset.filter(category_id=self.kwargs.get("pk"))
        # return queryset
        if not  self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset



    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get("pk"))
        context_data['category_id'] = category_item.pk

        context_data['title'] = f'Собаки породы  - все наши породы {category_item.name}'
        return context_data


class DogCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Dog
    # fields = ('name', 'category',)
    form_class = DogForm
    permission_required = 'dogs.add_dog'
    success_url = reverse_lazy('dogs:categories')


    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogUpdateView(LoginRequiredMixin,UpdateView):
    model = Dog
    form_class = DogForm

    # success_url = reverse_lazy('dogs:categories')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return  self.object

    def get_success_url(self):
        return reverse('dogs:dog_update', args=[self.object.category.pk])

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ParentFormSet(instance=self.object)
        context_data['formset'] = formset
        # category_item = Category.objects.get(pk=self.kwargs.get("pk"))
        # context_data['category_id'] = category_item.pk
        #
        # context_data['title'] = f'Собаки породы  - все наши породы {category_item.name}'
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class DogDeleteView(LoginRequiredMixin,DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:categories')

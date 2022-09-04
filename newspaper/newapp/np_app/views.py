from datetime import datetime
from django.shortcuts import render, reverse, redirect


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .filters import PostFilter
from .forms import PostForm, UserForm
from .models import Post, Category, User


from django.http import HttpResponse
from django.views import View
from .tasks import post_now
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 10


@login_required
def add_subscribe(request, pk):
    subscriber = request.user
    subscriber.save()
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)
    return redirect('/news/')

# Список новостей
class PostList(ListView):
    logger.info('INFO')
    model = Post
    ordering = ['-time_create']
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news_.html'
    context_object_name = 'news_'

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта
        obj = cache.get(f'posts-{self.kwargs["pk"]}', None)# кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'posts-{self.kwargs["pk"]}', obj)

        return obj


class Search(ListView):
    model = Post
    ordering = ['time_create']
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_add.html'
    permission_required = ('np_app.add_post')
#
    def form_valid(self, form):
        post = form.save()
        post_now.apply_async([post.pk], countdown=10)
        return redirect('/news/')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_add.html'
    permission_required = ('np_app.change_post')
#
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news/'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    form_class = UserForm
    success_url = reverse_lazy('news_list')

    def get_object(self, **kwargs):
        return self.request.user


class IndexView(View):
    def get(self, request):
        notify_new_post.delay()
        weekly_send_subscribers.delay()
        return HttpResponse('Hello!')



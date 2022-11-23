from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Reply, Mailing
from .forms import PostForm, ReplyForm, MailingForm
from .filters import PostFilter, ReplyFilter


@permission_required('polls.add_choice', raise_exception=True)
@login_required
def my_view(request):
    return HttpResponse()


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                          queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return redirect('/posts/')


class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class ReplyCreate(LoginRequiredMixin, CreateView):
    template_name = 'reply_create.html'
    form_class = ReplyForm
    success_url = '/posts/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        pk = self.kwargs.get('pk')
        obj.post = Post.objects.get(id=pk)
        obj.save()
        return redirect('/posts/reply/' + str(pk))


class PostReplyList(ListView):
    model = Reply
    template_name = 'reply.html'
    context_object_name = 'replyses'

    def get_queryset(self):
        return Reply.objects.filter(post__pk=self.kwargs.get('pk'))


class PersonalReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'personal_reply.html'
    context_object_name = 'replyses'

    def get_queryset(self):
        return Reply.objects.filter(post__author=self.request.user)

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ReplyFilter(self.request.GET,
                                          queryset=self.get_queryset())
        return context


class ReplyDelete(LoginRequiredMixin, DeleteView):
    template_name = 'reply_delete.html'
    queryset = Reply.objects.all()
    success_url = '/posts/personal_reply/'


class MailingCreate(LoginRequiredMixin, CreateView):
    template_name = 'mailing.html'
    form_class = MailingForm
    success_url = '/posts/'


@login_required
def add_accept(request, pk):
    obj = Reply.objects.get(id=pk)
    obj.status = True
    obj.save()
    return redirect('/posts/personal_reply/')
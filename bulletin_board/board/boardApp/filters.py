from django_filters import FilterSet
from .models import Post, Reply


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'category')


class ReplyFilter(FilterSet):

    class Meta:
        model = Reply
        fields = ('__all__')
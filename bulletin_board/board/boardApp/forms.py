from django.forms import ModelForm
from .models import Post, Reply, Mailing


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'upload']


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        fields = ['text']


class MailingForm(ModelForm):

    class Meta:
        model = Mailing
        fields = ['subject', 'text']
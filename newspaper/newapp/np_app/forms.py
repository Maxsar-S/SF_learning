from django import forms
from django.core.exceptions import ValidationError

from .models import Post, User, Category


class PostForm(forms.ModelForm):
    post_text = forms.CharField(min_length=15)

    class Meta:
        model = Post
        fields= [
            'title',
            'author',
            'post_category',
            'post_text',
        ]

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get("title")
            post_text = cleaned_data.get("post_text")

            if title == post_text:
                raise ValidationError("Описание не должно быть идентично названию")

            return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    #date = DateFilter(field_name='time_create', lookup_expr='gt', label='Date from',\
                      #widget=django.forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'title': ['icontains'],
            'time_create': ['gt']
        }
import datetime
from datetime import datetime
import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    date_post = django_filters.DateFilter(
        field_name='date_post',
        lookup_expr='gte',
        label='Не ранее',
        input_formats=['%d.%m.%Y']
    )
    title_post = django_filters.CharFilter(
        field_name='title_post',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )
    author_post = django_filters.CharFilter(
        field_name='author_post__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    class Meta:
        model = Post
        fields = ('title_post', 'date_post', 'author_post')

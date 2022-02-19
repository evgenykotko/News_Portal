from django.forms import ModelForm
from .models import Post


class AddNewsForm(ModelForm):

    class Meta:
        model = Post
        # fields = ['type_post', 'title_post', 'body_post', 'author_post', 'category_post']
        fields = '__all__'

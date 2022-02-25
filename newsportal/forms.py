from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post


class AddNewsForm(ModelForm):

    class Meta:
        model = Post
        # fields = ['type_post', 'title_post', 'body_post', 'author_post', 'category_post']
        fields = '__all__'


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
    
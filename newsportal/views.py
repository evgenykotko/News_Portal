from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.paginator import Paginator
from .models import Post, Author
from .filters import PostFilter
from .forms import AddNewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from datetime import datetime

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by("-id")
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news')

class NewsPost(DetailView):
    model = Post
    template_name = 'newspost.html'
    context_object_name = 'newspost'
    queryset = Post.objects.all()

class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AddNews(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    template_name = 'addnews.html'
    form_class = AddNewsForm

class UpdateNews(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    permission_required = ('newsportal.change_post')
    template_name = 'addnews.html'
    form_class = AddNewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class DeleteNews(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    permission_required = ('newsportal.delete_post')
    template_name = 'deletenews.html'
    context_object_name = 'newspost'
    queryset = Post.objects.all()
    success_url = '/news/search'

class IndexView(TemplateView):
    template_name = 'index.html'

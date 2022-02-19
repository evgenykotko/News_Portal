from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Post
from .filters import PostFilter
from .forms import AddNewsForm
from datetime import datetime

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by("-id")
    paginate_by = 10

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

class AddNews(CreateView):
    template_name = 'addnews.html'
    form_class = AddNewsForm

class UpdateNews(UpdateView):
    template_name = 'addnews.html'
    form_class = AddNewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class DeleteNews(DeleteView):
    template_name = 'deletenews.html'
    context_object_name = 'newspost'
    queryset = Post.objects.all()
    success_url = '/news/search'
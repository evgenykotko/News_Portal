from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type_post="news").order_by("-id")


class NewsPost(DetailView):
    model = Post
    template_name = 'newspost.html'
    context_object_name = 'newspost'
    queryset = Post.objects.all()
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.paginator import Paginator
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import AddNewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .signals import check_over_post_today


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'count_posts': Paginator(Post.objects.all().order_by('-id'), 1),
            'is_not_author': not self.request.user.groups.filter(name='author').exists(),
        }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['count_posts'] = Paginator(Post.objects.all(), 1)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
    #     return context


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

    def get_context_data(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        cat_list = []
        cats = Category.objects.filter(post__pk=id, subscribers=self.request.user).values('name')
        for cat in cats:
            cat_list.append(cat['name'])
        return {
            **super().get_context_data(*args, **kwargs),
            'list_cats': cat_list,
        }

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

@login_required
def subscribe(request, pk):
    user_id = request.user.id
    cat_name = request.POST['category']
    if not Category.objects.filter(post=pk, subscribers=request.user, name=cat_name).exists():
        Category.objects.get(name=cat_name).subscribers.add(user_id)
        return HttpResponse(f"{request.user}, Вы подписались на новости в категории {cat_name}")



class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10


    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'count_posts': Paginator(Post.objects.all().order_by('-id'), 1),
        }


class AddNews(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    template_name = 'addnews.html'
    form_class = AddNewsForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            addnews = form.save(commit=False)
            addnews.author_post = Author.objects.get(user=self.request.user)
            notify = check_over_post_today(sender=Post, instance=addnews, **kwargs)
            if notify < 3:
                addnews.save()
            else:
                return HttpResponse(f"{self.request.user}, на сегодня достаточно, Вы не можете больше сегодня постить")
        return redirect(form.instance.get_absolute_url())


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





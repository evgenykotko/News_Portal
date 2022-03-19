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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        cat_list = []
        cats = Category.objects.filter(post__pk=id, subscribers=self.request.user).values('name')
        for cat in cats:
            cat_list.append(cat['name'])

        # context['not_subscribed'] = not Category.objects.filter(post__pk=id, subscribers=self.request.user).exists()
        context['list_cats'] = cat_list
        return context

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
    if Category.objects.filter(post=pk, subscribers=request.user, name=cat_name).exists():
        return HttpResponse(f"{request.user}, Вы уже подписаны на новости в категории {cat_name}")
    else:
        Category.objects.get(name=cat_name).subscribers.add(user_id)
        return HttpResponse(f"{request.user}, Вы подписались на новости в категории {cat_name}")



class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class AddNews(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    template_name = 'addnews.html'
    form_class = AddNewsForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
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





from django.urls import path
from .views import NewsList, NewsPost, NewsSearch, AddNews, UpdateNews, DeleteNews, upgrade_me, subscribe

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('addnews/', AddNews.as_view(), name='news_add'),
    path('<int:pk>', NewsPost.as_view(), name='news_detail'),
    path('addnews/<int:pk>/', UpdateNews.as_view(), name='news_update'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
]

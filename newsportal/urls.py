from django.urls import path
from .views import NewsList, NewsPost, NewsSearch, AddNews, UpdateNews, DeleteNews, upgrade_me

urlpatterns = [
    path('', NewsList.as_view()),
    path('search/', NewsSearch.as_view()),
    path('addnews/', AddNews.as_view()),
    path('<int:pk>', NewsPost.as_view(), name='news_detail'),
    path('addnews/<int:pk>/', UpdateNews.as_view(), name='news_update'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade')

]

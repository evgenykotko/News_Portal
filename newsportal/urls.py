from django.urls import path
from .views import NewsList, NewsPost


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsPost.as_view()),
]

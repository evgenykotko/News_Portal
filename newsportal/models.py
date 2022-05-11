from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache



class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post = list(Post.objects.filter(author_post__pk=self.pk).values("rate_post"))
        commtopost = list(Comment.objects.filter(post__author_post__pk=self.pk).values("rate_comm"))
        commuser = list(Comment.objects.filter(user__author=self.pk).values("rate_comm"))
        a = 0
        b = 0
        c = 0
        for i in range(len(post)):
            a += post[i]['rate_post']
        for j in range(len(commtopost)):
            b += commtopost[j]['rate_comm']
        for k in range(len(commuser)):
            c += commuser[k]['rate_comm']
        self.rating = (3*a) + b + c
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User)
    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    post = 'post'
    news = 'news'
    TYPE_POST = [
        (post, 'Post'),
        (news, 'News'),
    ]
    date_post = models.DateTimeField(auto_now_add=True)
    type_post = models.CharField(max_length=4, choices=TYPE_POST, default=post)
    title_post = models.TextField()
    body_post = models.TextField()
    rate_post = models.IntegerField(default=0)
    author_post = models.ForeignKey("Author", on_delete=models.CASCADE)
    category_post = models.ManyToManyField(Category)

    def like(self):
        self.rate_post += 1
        self.save()

    def dislike(self):
        self.rate_post -= 1
        self.save()

    def preview(self):
        return self.body_post[:124] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def __str__(self):
        return f'{self.pk} - {self.title_post}'


class Comment(models.Model):
    date_comm = models.DateTimeField(auto_now_add=True)
    text_comm = models.TextField()
    rate_comm = models.IntegerField(default=0)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate_comm += 1
        self.save()

    def dislike(self):
        self.rate_comm -= 1
        self.save()
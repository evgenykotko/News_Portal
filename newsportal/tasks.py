from datetime import datetime, timedelta
from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
from django.contrib.auth.models import User


@shared_task
def new_posts(pk, nw):

    post = Post.objects.get(pk=pk)
    category = Category.objects.filter(post__pk=pk).values('name')
    for cat in category:
        subscribers = Category.objects.filter(name=cat['name']).values('subscribers__email')
        for email in subscribers:
            user = User.objects.get(email=email['subscribers__email'])
            html_content = render_to_string(
                'celery_post_subscribers.html',
                {
                    'post': post,
                    'user': user,
                    'nw': nw,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f"(Celery) В категории: {cat['name']} {nw} пост",
                body=f"{post.body_post[:50]}",
                to=[email['subscribers__email']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def mailing_week_posts():
    category = Category.objects.all().values('pk', 'name')
    for cat in category:
        subscribers = Category.objects.filter(name=cat['name']).values('subscribers__email')
        for email in subscribers:
            user = User.objects.get(email=email['subscribers__email'])
            week_posts = Post.objects.filter(
                category_post=cat['pk']
            ).exclude(
                date_post__lte=datetime.now()-timedelta(weeks=1)
            )
            if week_posts.exists():
                html_content = render_to_string(
                    'week_post_subscribers.html',
                    {
                        'week_posts': week_posts,
                        'user': user,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f"Еженедельная рассылка в категории {cat['name']}",
                    body='w_post.body_post for w_post in week_posts',
                    to=[email['subscribers__email']]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

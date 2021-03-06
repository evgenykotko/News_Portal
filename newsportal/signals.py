from datetime import datetime, timedelta

from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from .models import Post
from .tasks import new_posts


@receiver(pre_save, sender=Post)
def check_over_post_today(sender, instance, **kwargs):
    today_posts = Post.objects.filter(author_post=instance.author_post).exclude(
        date_post__lte=datetime.now()-timedelta(days=1)
    )
    return len(today_posts)

@receiver(post_save, sender=Post)
def notify_update_post(sender, instance, created, **kwargs):
    if not created:
        pk = instance.pk
        nw = 'обновился'
        new_posts.delay(pk, nw)


@receiver(m2m_changed, sender=Post.category_post.through)
def notify_subscriber(instance, action, **kwargs):
    if action == 'post_add':
        pk = instance.pk
        nw = 'новый'
        new_posts.delay(pk, nw)

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from .models import Post, Category
from django.contrib.auth.models import User

from django.template.loader import render_to_string

@receiver(post_save, sender=Post)
def notify_update_post(sender, instance, created, **kwargs):
    if not created:
        category = Category.objects.filter(post__pk=instance.pk).values('name')
        for cat in category:
            subscribers = Category.objects.filter(name=cat['name']).values('subscribers__email')
            for email in subscribers:
                user = User.objects.get(email=email['subscribers__email'])
                print(f'Отправлено: {user}')
                # html_content = render_to_string(
                #     'post_subscribers.html',
                #     {
                #         'instance': instance,
                #         'user': user,
                #     }
                # )
                #
                # msg = EmailMultiAlternatives(
                #     subject=f"В категории: {cat['name']} обновился пост: {instance.title_post}",
                #     body=f"{instance.body_post[:50]}",
                #     to=[email['subscribers__email']]
                # )
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

@receiver(m2m_changed, sender=Post.category_post.through)
def notify_subscriber(instance, action, **kwargs):
    if action == 'post_add':
        category = Category.objects.filter(post__pk=instance.pk).values('name')
        for cat in category:
            subscribers = Category.objects.filter(name=cat['name']).values('subscribers__email')
            for email in subscribers:
                user = User.objects.get(email=email['subscribers__email'])
                print(f'Отправлено: {user}')
                # html_content = render_to_string(
                #     'post_subscribers.html',
                #     {
                #         'instance': instance,
                #         'user': user,
                #     }
                # )
                #
                # msg = EmailMultiAlternatives(
                #     subject=f"В категории: {cat['name']} новый пост: {instance.title_post}",
                #     body=f"{instance.body_post[:50]}",
                #     to=[email['subscribers__email']]
                # )
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

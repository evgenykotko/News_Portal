# runapscheduler.py
import logging

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from newsportal.models import Post, Author, Category, PostCategory



logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    dt = date.today() # текущая дата
    ddt = (dt.isocalendar().week) # текущий номер недели
    category = Category.objects.all().values('pk', 'name') # отбираем все категории и забираем из них pk и name - (name не обязательно, просто для понимания как оно работает)
    for cat in category: # перебираем категории циклом
        print('-------')
        print(f"--{cat['name']}") # по сути name нужен только тут
        subscribers = Category.objects.filter(name=cat['pk']).values('subscribers__email') # выбираем адреса всех подписчиков данной категории
        for email in subscribers: # перебираем адреса циклом
            print(f"----{email['subscribers__email']}")
            user = User.objects.get(email=email['subscribers__email']) # попутно, на основании адресов выбираем username, это для корректного обращения в письме.
            week_posts = Post.objects.filter(date_post__week__gte=(ddt-1), date_post__week__lte=ddt, category_post=cat['pk']) # и вот он - костыль и он же весь смысл функции :)
            # выбираются посты в промежутке от прошлой недели (ddt-1) до текущей недели (ddt) и выбранной категории
            # т.о. у нас есть адреса: email['subscribers__email'], есть имена: user и есть посты за неделю: week_posts
            # все это впихиваем в рассылку:
            print(f"{week_posts}")

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

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),  # В пятницу, в 18:00
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
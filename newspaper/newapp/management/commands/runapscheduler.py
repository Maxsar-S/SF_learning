import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from newapp.models import User, Category, Post
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# задача по выводу текста на экран
def my_job():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.datetime.now().isocalendar()[1] - 1

        for news in Post.objects.filter(post_category=category.id,
                                        time_create__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'time_create',
                                                                                    'post_category__name'):
            date_format = news.get("time_create").strftime("%m/%d/%Y")

            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Category: {news.get("post_category__name")}, Date creation: {date_format}')

            news_from_each_category.append(new)
        print()
        print('+++++++++++++++++++++++++++++', category.name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("Письма будут отправлены подписчикам категории:", category.name, '( id:', category.id, ')')

        # переменная subscribers содержит информацию по подписчиках, в дальшейшем будет использоваться их почта
        subscribers = category.subscribers.all()

        # цикл для вывода информации в консоль об адресах подписчиков (для тестов)
        print('по следующим адресам email: ')
        for qaz in subscribers:
            print(qaz.email)

        print()
        print()

        for subscriber in subscribers:
            print('____________________________', subscriber.email, '___________________________________')
            print()
            print('Письмо, отправленное по адресу: ', subscriber.email)
            html_content = render_to_string(
                'sender.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Для {subscriber.username.title} новые посты в Вашей любимой категории',
                from_email='kavrsflearning@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()

            # вывод в консоль содержимого письма для проверки содержимого и адресата отправления
            print(html_content)

            # Чтобы запустить рассылку, нужно раскоментить нижнюю строчку
            msg.send()

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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

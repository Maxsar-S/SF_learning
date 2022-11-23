from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Reply, Mailing


@receiver(post_save, sender=Reply)
def notify_reply(sender, instance, created, **kwargs):
    if created:
        subject = f'Добавлен отклик {instance.post} {instance.text} {instance.author}'
        recipient = instance.post.author.email
    else:
        if instance.status:
            subject = f'Ваш отклик принят {instance.post} {instance.text} {instance.author}'
            recipient = instance.author.email
    send_mail(
        subject=subject,
        message=instance.text,
        from_email='kavrsflearning@yandex.ru',
        recipient_list=[recipient],
    )


@receiver(post_save, sender=Mailing)
def mailing(sender, instance, created, **kwargs):
    if created:
        for recipient in User.objects.all():
            send_mail(
                subject=instance.subject,
                message=instance.text,
                from_email='kavrsflearning@yandex.ru',
                recipient_list=[recipient.email],
            )
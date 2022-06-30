from django.shortcuts import redirect

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Post, Category, User


@receiver(m2m_changed, sender=Post.post_category.through)
def notyfication_new_post(sender, instance, *args, **kwargs):
    for cat_id in instance.post_category.all():
        users = Category.objects.filter(pk=cat_id.id).values("subscribers")
        for user_id in users:
            send_mail(
                subject=f'{instance.title}',
                message=f'Вашему вниманию {User.objects.get(pk=user_id["subscribers"]).username}!'
                        f'Новый пост \n'
                        f'{instance.title} : {instance.post_text[0:5]}  \n'
                        f'Для прочтения новости полностью проследуйте по ссылке http://127.0.0.1:8000/news/{instance.id}',
                from_email='kavrsflearning@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id["subscribers"]).email]
            )

            return redirect('/news/')

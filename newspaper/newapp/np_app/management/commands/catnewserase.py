from django.core.management.base import BaseCommand, CommandError
from np_app.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет новости из какой-либо категории при подтверждении действия в консоли выполнения команды'

    def add_arguments(self, parser):
        parser.add_argument('post_category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все статьи в категории {options["post_category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Удаление отменено'))

        try:
            post_category = Category.objects.get(name=options['post_category'])
            Post.objects.filter(post_category==post_category).delete()
            self.stdout.write(self.style.SUCCESS('Успешно удалены все новости из категории {post_category.name}'))

        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не могу найти категорию'))




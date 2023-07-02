from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def send_congratulations(post):
    send_mail(
        'Поздравляем с достижением 100 просмотров',
        f'Ваша статья {post.title} достигла 100 просмотров. Поздравляем!',
        settings.EMAIL_HOST_USER,
        recipient_list=['ваш имэил'],
        fail_silently=False,
    )

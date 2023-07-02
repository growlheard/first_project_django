from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


def send_congratulations(post):
    send_mail(
        '����������� � ����������� 100 ����������',
        f'���� ������ {post.title} �������� 100 ����������. �����������!',
        settings.EMAIL_HOST_USER,
        recipient_list=['��� �����'],
        fail_silently=False,
    )

from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from catalog.models import Post


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Test post', content='Test content')
        self.client = Client()

    def test_views_count_reaches_100(self):
        # Переходим на страницу статьи 99 раз
        for i in range(99):
            self.client.get(reverse('catalog:post_detail', args=[self.post.id]))
            self.post.refresh_from_db()
            self.assertEqual(self.post.views_count, i + 1)

            # Переходим на страницу статьи еще раз, чтобы достичь 100 просмотров
            response = self.client.get(reverse('catalog:post_detail', args=[self.post.id]))
            self.post.refresh_from_db()
            self.assertEqual(self.post.views_count, 100)

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Поздравляем с достижением 100 просмотров')
            self.assertEqual(mail.outbox[0].to, ['growlheard@gmail.com'])

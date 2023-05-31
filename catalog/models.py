from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(max_length=255, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    description = models.TextField(max_length=255, verbose_name='Описание Продукта', **NULLABLE)
    image = models.ImageField(upload_to='product_images/', verbose_name='', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} - {self.price}: {self.category}'

    class Meta:
        verbose_name = 'Название продукта'
        verbose_name_plural = 'Название продуктов'
        ordering = ('name',)


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Url', blank=True)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog', null=True, blank=True, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        print('Saving post:', self.title)
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = 'Записи в блоге'
        ordering = ['-created_at']

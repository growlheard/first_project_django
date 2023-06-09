# Generated by Django 4.2.1 on 2023-05-13 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(max_length=255, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('description', models.TextField(max_length=255, verbose_name='Описание Продукта')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена за покупку')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Название продукта',
                'verbose_name_plural': 'Название продуктов',
                'ordering': ('name',),
            },
        ),
    ]

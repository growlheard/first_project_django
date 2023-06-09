from django.core.management import BaseCommand, call_command
from catalog.models import Category, Product
from django.core.management.commands.loaddata import Command as LoaddataCommand


class Command(BaseCommand):
    help = 'Загружает данные каталога из json файла'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Открываем файл в бинарном режиме и читаем его содержимое
        with open('catalog_data.json', 'rb') as f:
            json_data = f.read()

        # Заменяем все Null-байты на пустые строки
        json_data = json_data.replace(b'\x00', b'')

        # Записываем измененное содержимое в новый временный файл
        with open('catalog_data_temp.json', 'wb') as f:
            f.write(json_data)

        # Загружаем данные из временного файла
        loaddata_cmd = LoaddataCommand()
        loaddata_cmd.execute('catalog_data_temp.json')

        # Удаляем временный файл
        os.remove('catalog_data_temp.json')

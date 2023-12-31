from csv import DictReader

from categories.models import Category, Group, Product, Subcategory
from django.core.management.base import BaseCommand
from stores.models import City, Division, Store

data_dir = 'initial_data'


csv_files = [
    {'model': Group, 'filename': 'pr_df.csv',
     'fieldnames': ['pass', 'title']},
    {'model': Category, 'filename': 'pr_df.csv',
     'fieldnames': ['pass', 'group', 'title']},
    {'model': Subcategory, 'filename': 'pr_df.csv',
     'fieldnames': ['pass', 'pass', 'category', 'title']},
    {'model': Product, 'filename': 'pr_df.csv',
     'fieldnames': ['sku', 'pass', 'pass', 'subcategory', 'uom']},
    {'model': City, 'filename': 'st_df.csv',
     'fieldnames': ['pass', 'city']},
    {'model': Division, 'filename': 'st_df.csv',
     'fieldnames': ['pass', 'pass', 'division']},
    {'model': Store, 'filename': 'st_df.csv',
     'fieldnames': [
         'store', 'city', 'division', 'type_format', 'loc', 'size', 'is_active'
         ]},
]


class Command(BaseCommand):
    help = "Загружает данные из файлов csv"

    def add_group(self, row):
        """Создает или обновляет группу."""
        Group.objects.update_or_create(title=row['title'],)

    def add_category(self, row):
        """Создает или обновляет категорию."""
        Category.objects.update_or_create(
            title=row['title'],
            group=Group.objects.filter(title=row['group']).first(),
        )

    def add_subcategory(self, row):
        """Создает или обновляет подкатегорию."""
        Subcategory.objects.update_or_create(
            title=row['title'],
            category=Category.objects.filter(title=row['category']).first(),
        )

    def add_product(self, row):
        """Создает или обновляет продукт."""
        Product.objects.update_or_create(
            sku=row['sku'],
            subcategory=Subcategory.objects.filter(title=row['subcategory']).first(),
            uom=row['uom'],
        )

    def add_city(self, row):
        """Создает или обновляет город."""
        City.objects.update_or_create(city=row['city'])

    def add_division(self, row):
        """Создает или обновляет отдел."""
        Division.objects.update_or_create(division=row['division'])

    def add_store(self, row):
        """Создает или обновляет магазин."""
        Store.objects.update_or_create(
            store=row['store'],
            city=City.objects.filter(city=row['city']).first(),
            division=Division.objects.filter(division=row['division']).first(),
            type_format=row['type_format'],
            loc=row['loc'],
            size=row['size'],
            is_active=row['is_active'],
        )

    def csv_loader(self, cf):
        csv_file = f'{data_dir}/{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            if cf['model'] == Group:
                create_func = self.add_group
            elif cf['model'] == Category:
                create_func = self.add_category
            elif cf['model'] == Subcategory:
                create_func = self.add_subcategory
            elif cf['model'] == Product:
                create_func = self.add_product
            elif cf['model'] == City:
                create_func = self.add_city
            elif cf['model'] == Division:
                create_func = self.add_division
            elif cf['model'] == Store:
                create_func = self.add_store

            i, err, r = 0, 0, 0
            next(reader)
            for row in reader:
                try:
                    create_func(row)
                    r += 1
                except Exception as error:
                    print(row)
                    print(
                        f'Ошибка записи в таблицу модели '
                        f'{cf["model"].__name__}, '
                        f'{str(error)}')
                    err += 1
                i += 1
            print(
                f'Всего: {i} строк. Загружено: {r} строк. '
                f'Ошибки: {err} строк.')

    def handle(self, *args, **options):
        print("Идет загрузка данных")
        for сf in csv_files:
            self.csv_loader(сf)
        print('Загрука завершена.')

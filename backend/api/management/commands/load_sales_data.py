import time
from csv import DictReader

from categories.models import Product
from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update
from sales.models import Sale
from stores.models import Store

data_dir = 'initial_data'

csv_files = [
    {'model': Sale, 'filename': 'sales_df_train.csv',
     'fieldnames': [
         'store', 'sku', 'date', 'sales_type', 'sales_units',
         'sales_units_promo', 'sales_rub', 'sales_rub_promo'
     ]
     },
]

MAX_ROWS = 1000  # Максимальное количество строк для одновременной загрузки


class Command(BaseCommand):
    """Загружает или обновляет данные из файлов csv."""

    def calculate_execution_time(func):
        """Выводит время выполнения функции."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Время выполнения функции {func.__name__}: {execution_time} секунд")
            return result
        return wrapper

    def add_sale(self, rows):
        """Создает или обновляет записи о продаже товара."""
        sales = []
        sales_for_update = []
        for row in rows:
            # Находим существующий объект продажи, если он существует
            sale = (
                Sale.objects.filter(
                    store=row['store'], sku=row['sku'], date=row['date']
                ).first()
            )
            if not sale:
                # Создаем новый объект продажи
                sale = Sale(
                    store=Store.objects.filter(store=row['store']).first(),
                    sku=Product.objects.filter(sku=row['sku']).first(),
                    date=row['date'],
                    sales_type=row['sales_type'],
                    sales_units=row['sales_units'],
                    sales_units_promo=row['sales_units_promo'],
                    sales_rub=row['sales_rub'],
                    sales_rub_promo=row['sales_rub_promo'],
                )
                sales.append(sale)
            else:
                # Обновляем существующий объект продажи
                sale.date = row['date']
                sale.sales_type = row['sales_type']
                sale.sales_units = row['sales_units']
                sale.sales_units_promo = row['sales_units_promo']
                sale.sales_rub = row['sales_rub']
                sale.sales_rub_promo = row['sales_rub_promo']
                sales_for_update.append(sale)
        Sale.objects.bulk_create(sales)
        bulk_update(sales_for_update, update_fields=[
            'date', 'sales_type', 'sales_units', 'sales_units_promo',
            'sales_rub', 'sales_rub_promo'
        ])

    def csv_loader(self, cf):
        csv_file = f'{data_dir}/{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            create_func = self.add_sale

            i, err, r = 0, 0, 0
            next(reader)
            rows = []
            for row in reader:
                try:
                    rows.append(row)
                    if len(rows) >= MAX_ROWS:
                        create_func(rows)
                        r += len(rows)
                        rows = []
                except Exception as error:
                    print(row)
                    print(
                        f'Ошибка записи в таблицу модели '
                        f'{cf["model"].__name__}, '
                        f'{str(error)}')
                    err += 1
                i += 1
            if rows:
                create_func(rows)
                r += len(rows)
            print(
                f'Всего: {i} строк. Загружено или обновлено: {r} строк. '
                f'Ошибки: {err} строк.')

    @calculate_execution_time
    def handle(self, *args, **options):
        print("Идет загрузка данных")
        for сf in csv_files:
            self.csv_loader(сf)
        print('Загрука завершена.')

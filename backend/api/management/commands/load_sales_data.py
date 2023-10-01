from csv import DictReader

from categories.models import Product
from django.core.management.base import BaseCommand
from sales.models import Sale
from stores.models import Store

data_dir = 'initial_data'

csv_files = [
    {'model': Sale, 'filename': 'sales_df_train_trim.csv',
     'fieldnames': [
         'store', 'sku', 'date', 'sales_type', 'sales_units',
         'sales_units_promo', 'sales_rub', 'sales_rub_promo'
     ]
     },
]


class Command(BaseCommand):
    help = "Загружает данные из файлов csv"

    def add_sale(self, row):
        """Создает или обновляет запись о продаже товара."""
        Sale.objects.update_or_create(
            store=Store.objects.filter(store=row['store']).first(),
            sku=Product.objects.filter(sku=row['sku']).first(),
            date=row['date'],
            sales_type=row['sales_type'],
            sales_units=row['sales_units'],
            sales_units_promo=row['sales_units_promo'],
            sales_rub=row['sales_rub'],
            sales_rub_promo=row['sales_rub_promo'],
        )

    def csv_loader(self, cf):
        csv_file = f'{data_dir}/{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            create_func = self.add_sale

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

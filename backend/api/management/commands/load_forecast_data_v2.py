import time
from csv import DictReader

from categories.models import Product
from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update
from sales_forecasts.models import Forecast
from stores.models import Store

from .time_counter import calculate_execution_time

data_dir = 'initial_data'

csv_files = [
    {'model': Forecast, 'filename': 'sales_submission_test.csv',
     'fieldnames': ['store', 'sku', 'date', 'target']},
]

MAX_ROWS = 1000  # Максимальное количество строк для одновременной загрузки
FORECAST_DATE = '2023-07-19'  # Дата прогноза, предоставленная в начальных данных.
                              # При загрузке других прогнозов, необходимо изменить дату.


class Command(BaseCommand):
    """Загружает или обновляет данные из файлов csv."""

    def add_forecast(self, rows):
        """Создает или обновляет записи о прогнозе продажи товара."""
        forecasts = []
        forecasts_for_update = []
        for row in rows:
            # Находим существующий объект прогноза, если он существует
            forecast = (
                Forecast.objects.filter(
                    forecast_date=FORECAST_DATE,
                    store=row['store'],
                    sku=row['sku'],
                    date=row['date']
                ).first()
            )
            if not forecast:
                # Создаем новый объект прогноза
                forecast = Forecast(
                    forecast_date=FORECAST_DATE,
                    store=Store.objects.filter(store=row['store']).first(),
                    sku=Product.objects.filter(sku=row['sku']).first(),
                    date=row['date'],
                    target=row['target']
                )
                forecasts.append(forecast)
            else:
                # Обновляем существующий объект прогноза
                forecast.target = row['target']
                forecasts_for_update.append(forecast)
        Forecast.objects.bulk_create(forecasts)
        bulk_update(forecasts_for_update, update_fields=['target'])

    def csv_loader(self, cf):
        csv_file = f'{data_dir}/{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            create_func = self.add_forecast

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

import time
from csv import DictReader

from categories.models import Product
from django.core.management.base import BaseCommand
from django_bulk_update.helper import bulk_update
from sales_forecasts.models import Forecast, ForecastDaily, ForecastSku
from stores.models import Store

data_dir = 'initial_data'

csv_files = [
    {'model': Forecast, 'filename': 'sales_submission.csv',
     'fieldnames': ['store']},
    {'model': ForecastSku, 'filename': 'sales_submission.csv',
     'fieldnames': ['store', 'sku']},
    {'model': ForecastDaily, 'filename': 'sales_submission.csv',
     'fieldnames': ['store', 'sku', 'date', 'target']},
]

MAX_ROWS = 1000  # Максимальное количество строк для одновременной загрузки
FORECAST_DATE = '2023-07-19'  # Дата прогноза, предоставленная в начальных
# данных. При загрузке других прогнозов, необходимо изменить дату.


class Command(BaseCommand):
    """Загружает или обновляет данные из файлов csv."""

    def calculate_execution_time(func):
        """Выводит время выполнения функции."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Время выполнения функции {func.__name__}: "
                  f"{execution_time} секунд.")
            return result
        return wrapper

    def add_forecast(self, rows):
        """Создает записи о прогнозе продаж магазина на дату."""
        forecasts = []
        unique_forecasts = []
        for row in rows:
            # Находим существующий объект прогноза, если он существует
            forecast = (
                Forecast.objects.filter(
                    store=row['store'],
                    forecast_date=FORECAST_DATE,
                ).first()
            )
            if not forecast:
                # Создаем новый объект продажи
                forecast = Forecast(
                    store=Store.objects.filter(store=row['store']).first(),
                    forecast_date=FORECAST_DATE,
                )
                unique_forecast = {
                    row['store']: FORECAST_DATE
                }
                if unique_forecast not in unique_forecasts:
                    forecasts.append(forecast)
                    unique_forecasts.append(unique_forecast)
        Forecast.objects.bulk_create(forecasts)

    def add_forecast_sku(self, rows):
        """Создает записи о продаже товара в магазине на дату."""
        forecasts_sku = []
        unique_forecasts_sku = []
        for row in rows:
            # Находим существующий объект магазин-товар, если он существует
            forecast_sku = (
                ForecastSku.objects.filter(
                    forecast__store=row['store'],
                    forecast__forecast_date=FORECAST_DATE,
                    sku__sku=row['sku'],
                ).first()
            )
            if not forecast_sku:
                unique_forecast_sku = {
                    row['store']: row['sku']
                }
                if unique_forecast_sku not in unique_forecasts_sku:
                    forecast_sku = ForecastSku(
                        forecast=Forecast.objects.filter(
                            store=row['store'],
                            forecast_date=FORECAST_DATE,
                        ).first(),
                        sku=Product.objects.filter(sku=row['sku']).first(),
                    )
                    forecasts_sku.append(forecast_sku)
                    unique_forecasts_sku.append(unique_forecast_sku)
        ForecastSku.objects.bulk_create(forecasts_sku)

    def add_forecast_daily(self, rows):
        """Создает записи о ежедневном прогнозе продаж 
        продукта в магазина на разные даты."""
        forecasts_daily = []
        forecasts_daily_to_update = []
        for row in rows:
            # Находим существующий объект прогноза, если он существует
            forecast_daily = (
                ForecastDaily.objects.filter(
                    sales_units__forecast__store=row['store'],
                    sales_units__sku__sku=row['sku'],
                    sales_units__forecast__forecast_date=FORECAST_DATE,
                    date=row['date'],
                ).first()
            )
            if not forecast_daily:
                forecast_daily = ForecastDaily(
                    sales_units=ForecastSku.objects.filter(
                        forecast__store__store=row['store'],
                        forecast__forecast_date=FORECAST_DATE,
                        sku__sku=row['sku'],
                    ).first(),
                    date=row['date'],
                    target=row['target'],
                )
                forecasts_daily.append(forecast_daily)
            else:
                # Обновляем существующий объект прогноза
                forecast_daily.sales_units = ForecastSku.objects.filter(
                    forecast__store__store=row['store'],
                    forecast__forecast_date=FORECAST_DATE,
                    sku__sku=row['sku'],
                ),
                forecast_daily.date = row['date'],
                forecast_daily.target = row['target']
                forecasts_daily_to_update.append(forecast_daily)
        ForecastDaily.objects.bulk_create(forecasts_daily)
        bulk_update(forecasts_daily_to_update, update_fields=[
            'sales_units', 'date', 'target'
        ])

    def csv_loader(self, cf):
        csv_file = f'{data_dir}/{cf["filename"]}'
        with open(csv_file, encoding='utf-8', newline='') as csvfile:
            reader = DictReader(csvfile, fieldnames=cf['fieldnames'])
            print(f'Загрузка в таблицу модели {cf["model"].__name__}')

            if cf['model'] == Forecast:
                create_func = self.add_forecast
            elif cf['model'] == ForecastSku:
                create_func = self.add_forecast_sku
            elif cf['model'] == ForecastDaily:
                create_func = self.add_forecast_daily

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

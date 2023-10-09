import csv
import datetime
from csv import DictReader

from categories.models import Product
from django.db import models
from django.http import HttpResponse
from django_bulk_update.helper import bulk_update
from rest_framework import status
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store

data_dir = '/backend_static'

sales_headers = [
    'st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
    'pr_sales_in_units', 'pr_promo_sales_in_units',
    'pr_sales_in_rub', 'pr_promo_sales_in_rub'
]

stores_headers = [
    'st_id', 'st_city_id', 'st_division_code', 'st_type_format_id',
    'st_type_loc_id', 'st_type_size_id', 'st_is_active'
]

products_headers = [
    'pr_sku_id', 'pr_group_id', 'pr_cat_id',
    'pr_subcat_id', 'pr_uom_id'
]

csv_files = [
    {'model': Sale, 'filename': 'uploaded_sales_data',
     'headers': sales_headers},
    {'model': Store, 'filename': 'uploaded_stores_data',
     'headers': stores_headers},
    {'model': Product, 'filename': 'uploaded_products_data',
     'headers': products_headers}
]

csv_file_forecast = {
    'model': Forecast,
    'filename': 'sales_submission_out.csv',
    'fieldnames': ['pass', 'store', 'sku', 'date', 'target']
}  # pass - заглушка, пока DS не сменят структуру файла


MAX_ROWS = 1000  # Максимальное количество строк для одновременной загрузки


def data_to_file(cf, request):
    """Скачивает данные о продажах в csv."""
    model = cf['model']
    if model == Sale:
        # выбор имени файла из запроса или по умолчанию
        file_name = request.GET.get('sales_file_name', cf.get('filename'))
        queryset = Sale.objects.all().order_by('store', 'sku', 'date')
    elif model == Store:
        file_name = request.GET.get('stores_file_name', cf.get('filename'))
        queryset = Store.objects.all().order_by('store')
    elif model == Product:
        file_name = request.GET.get('products_file_name', cf.get('filename'))
        queryset = Product.objects.all().order_by('sku').select_related(
            'subcategory__category__group',
            'subcategory__category'
        )
    # добавляем путь и расширение файла
    file_name = '/backend_static/' + file_name + '.csv'
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cf['headers'])
        fields = []
        for field in model._meta.get_fields():
            # добавляем поле модели в список, если оно не автоинициализировано,
            # а явно прописано
            if not field.auto_created:
                fields.append(field)
        rows = []
        counter = 0
        for obj in queryset:
            # добавляем значения полей в список
            # если поле модели является boolean, то приводим его к int
            row = [
                getattr(obj, field.name) if not isinstance(
                    field, models.BooleanField
                ) else int(getattr(obj, field.name)) for field in fields
            ]
            if model == Product:
                field = obj.subcategory.category.group.title
                row.insert(1, field)
                field = obj.subcategory.category.title
                row.insert(2, field)
            rows.append(row)
            counter += 1
            if len(rows) >= MAX_ROWS:
                writer.writerows(rows)
                rows = []
        if rows:
            writer.writerows(rows)
    if model == Sale:
        subject = 'Продажи'
    elif model == Store:
        subject = 'Магазины'
    elif model == Product:
        subject = 'Продукты'
    message = (
        f'{subject} записаны в файл {file_name}. Всего строк: {counter}. '
    )
    print(message)
    return message


def all_data_to_files(request):
    """Загружает данные о магазинах, товарах и продажах в csv."""
    messages = []
    for cf in csv_files:
        print('Идет выгрузка данных.')
        messages.append(data_to_file(cf, request))
    return HttpResponse(messages, status=status.HTTP_200_OK)


def add_forecast(rows):
    """Создает или обновляет записи о прогнозе продажи товара."""
    forecasts = []
    forecasts_for_update = []
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    for row in rows:
        # Находим существующий объект прогноза, если он существует
        forecast = (
            Forecast.objects.filter(
                forecast_date=current_date,
                store=row['store'],
                sku=row['sku'],
                date=row['date']
            ).first()
        )
        if not forecast:
            # Создаем новый объект прогноза
            forecast = Forecast(
                forecast_date=current_date,
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


def forecasts_loader():
    """Загружает или обновляет записи о прогнозе продаж товаров в БД."""
    csv_file = f'{data_dir}/{csv_file_forecast["filename"]}'
    with open(csv_file, encoding='utf-8', newline='') as csvfile:
        reader = DictReader(
            csvfile, fieldnames=csv_file_forecast['fieldnames']
        )

        create_func = add_forecast

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
                    f'{csv_file_forecast["model"].__name__}, '
                    f'{str(error)}')
                err += 1
            i += 1
        if rows:
            create_func(rows)
            r += len(rows)
        print(
            f'Всего: {i} строк. Загружено или обновлено: {r} строк. '
            f'Ошибки: {err} строк.')
        return HttpResponse('Прогноз загружен.', status=status.HTTP_200_OK)

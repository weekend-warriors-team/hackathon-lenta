import csv

from categories.models import Product
from django.db import models
from django.http import HttpResponse
from rest_framework import status
from sales.models import Sale
from stores.models import Store

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

MAX_ROWS = 1000


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
    message = f'{subject} записаны в файл {file_name}. Всего строк: {counter}. '
    print(message)
    return message


def all_data_to_files(request):
    """Загружает данные о магазинах, товарах и продажах в csv."""
    messages = []
    for cf in csv_files:
        print('Идет выгрузка данных.')
        messages.append(data_to_file(cf, request))
    return HttpResponse(messages, status=status.HTTP_200_OK)

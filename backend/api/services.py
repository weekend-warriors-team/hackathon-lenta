import csv

from django.http import HttpResponse
from rest_framework import status
from sales.models import Sale

sales_headers = [
    'st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
    'pr_sales_in_units', 'pr_promo_sales_in_units',
    'pr_sales_in_rub', 'pr_promo_sales_in_rub'
]

stores_headers = [
    'st_id', 'st_city_id', 'st_division_code', 'st_type_format_id',
    'st_type_loc_id', 'st_type_size_id', 'st_is_active'
]

categories_headers = [
    'pr_sku_id', 'pr_group_id', 'pr_cat_id',
    'pr_subcat_id', 'pr_uom_id'
]

MAX_ROWS = 1000


def sales_data_to_file(request):
    """Скачивает данные о продажах в csv."""
    file_name = '/backend_static/' + request.GET.get(
        'file_name', 'uploaded_sales_data'
    ) + '.csv'
    queryset = Sale.objects.all().order_by('store', 'sku', 'date')[:1000]
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(sales_headers)
        # получаем список полей модели Sale
        fields = [
            field for field in Sale._meta.get_fields()
            if field.name != 'id'
        ]
        rows = []
        counter = 0
        for sale in queryset:
            rows.append(
                [
                    getattr(sale, field.name) if field.name != 'sales_type'
                    else int(getattr(sale, field.name)) for field in fields
                ]
            )
            counter += 1
            if len(rows) >= MAX_ROWS:
                writer.writerows(rows)
                rows = []
        if rows:
            writer.writerows(rows)
    print(f'Продажи записаны в файл {file_name}. Всего строк: {counter}')
    return HttpResponse(
        f'Продажи записаны в файл {file_name}. Всего строк: {counter}',
        status=status.HTTP_200_OK
    )

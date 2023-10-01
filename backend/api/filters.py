from django_filters.rest_framework import FilterSet, filters
from sales.models import Sale
from stores.models import Store


class StoresFilter(filters.FilterSet):
    '''Фильтр магазинов.'''
    model = Store
    fields = ('store', 'city', 'division', 'type_format', 'loc',)


class SalesFilter(filters.FilterSet):
    '''Фильтр продаж'''
    model = Sale
    fields = ('store', 'date', 'sales_type', 'sales_units', 'sales_units_promo', 'sales_rub', 'sales_rub_promo')
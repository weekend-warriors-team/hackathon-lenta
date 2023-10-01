from django_filters.rest_framework import FilterSet as filters
from stores.models import Stores
from sales.models import Sales


class StoresFilter(filters.FilterSet):
    '''Фильтр магазинов'''
    model = Stores
    fields = ('store', 'city', 'division', 'type_format', 'loc')


class SalesFilter(filters.FilterSet):
    '''Фильтр продаж'''
    model = Sales
    fields = ('store', 'sku')

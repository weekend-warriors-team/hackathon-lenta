from django_filters.rest_framework import FilterSet, filters
from sales.models import Sales
from stores.models import Store


class StoresFilter(FilterSet):
    '''Фильтр магазинов.'''
    model = Store
    fields = ('store', 'city', 'division', 'type_format', 'loc',)

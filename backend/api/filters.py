from django_filters.rest_framework import FilterSet, filters
from sales.models import Sales
from stores.models import Stores


class StoresFilter(FilterSet):
    '''Фильтр магазинов.'''
    model = Stores
    fields = ('store', 'city', 'division', 'type_format', 'loc',)

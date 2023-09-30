from django_filters.rest_framework import FilterSet, filters
from stores.models import Stores
from sales.models import Sales


class StoresFilter(FilterSet):
    '''Фильтр продаж'''
    model = Stores
    fields = ('store', 'city', 'division', 'type_format', 'loc',)

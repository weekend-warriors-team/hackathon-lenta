from django_filters import rest_framework
from sales.models import Sale
from sales_forecasts.models import Forecast
from stores.models import Store


class StoresFilter(rest_framework.FilterSet):
    '''Фильтр магазинов.'''
    model = Store
    fields = ('store', 'city', 'division', 'type_format', 'loc',)


class SalesFilter(rest_framework.FilterSet):
    '''Фильтр продаж'''
    model = Sale
    fields = ('store', 'date', 'sales_type', 'sales_units', 'sales_units_promo', 'sales_rub', 'sales_rub_promo')


class ForecastFilter(rest_framework.FilterSet):
    """Фильтр прогноза продаж."""
    store = rest_framework.CharFilter(required=True)
    forecast_date = rest_framework.DateFilter(required=True,)

    class Meta:
        model = Forecast
        fields = ('store', 'sku', 'forecast_date')

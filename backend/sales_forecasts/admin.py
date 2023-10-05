from django.contrib import admin

from .models import Forecast


class ForecastAdmin(admin.ModelAdmin):
    """Админка данных прогноза продаж."""
    list_display = ('forecast_date', 'store', 'sku', 'date', 'target')
    search_fields = ('store__store', 'sku__sku',)
    list_filter = ('forecast_date', 'store', 'sku')
    empty_value_display = '-пусто-'


admin.site.register(Forecast, ForecastAdmin)

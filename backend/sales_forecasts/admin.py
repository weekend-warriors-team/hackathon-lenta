from django.contrib import admin

from .models import Forecast, ForecastDaily, ForecastSku


class ForecastAdmin(admin.ModelAdmin):
    '''Админка данных прогноза'''
    list_display = ('store', 'forecast_date')
    search_fields = ('forecast_date',)
    empty_value_display = '-пусто-'


class ForecastSkuAdmin(admin.ModelAdmin):
    '''Админка прогноза товаров'''
    list_display = ('forecast', 'sku')
    search_fields = ('sku__sku',)
    empty_value_display = '-пусто-'


class ForecastDailyAdmin(admin.ModelAdmin):
    '''Админка ежедневного прогноза товаров'''
    list_display = ('sales_units', 'date', 'target')
    search_fields = ('date',)
    empty_value_display = '-пусто-'


admin.site.register(Forecast, ForecastAdmin)
admin.site.register(ForecastSku, ForecastSkuAdmin)
admin.site.register(ForecastDaily, ForecastDailyAdmin)

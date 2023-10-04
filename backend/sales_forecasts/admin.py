from django.contrib import admin

from .models import Forecast


class ForecastAdmin(admin.ModelAdmin):
    """Админка данных прогноза продаж."""
    list_display = ('forecast_date', 'store', 'sku', 'date', 'target')
    search_fields = ('store__store', 'sku__sku',)
    list_filter = ('forecast_date', 'store', 'sku')
    empty_value_display = '-пусто-'


# class ForecastSkuAdmin(admin.ModelAdmin):
#     '''Админка прогноза товаров'''
#     list_display = ('forecast', 'sku')
#     search_fields = ('sku__sku',)
#     empty_value_display = '-пусто-'
# 
# 
# class ForecastDailyAdmin(admin.ModelAdmin):
#     '''Админка ежедневного прогноза товаров'''
#     list_display = ('sales_units', 'date', 'target')
#     search_fields = ('date',)
#     empty_value_display = '-пусто-'


admin.site.register(Forecast, ForecastAdmin)
# admin.site.register(ForecastSku, ForecastSkuAdmin)
# admin.site.register(ForecastDaily, ForecastDailyAdmin)

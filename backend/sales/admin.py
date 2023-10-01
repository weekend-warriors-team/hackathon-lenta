from django.contrib import admin


class SaleAdmin(admin.ModelAdmin):
    """Админка продаж"""
    list_display = ('store',  'sku', 'date', 'sales_type', 'sales_units', 
                    'sales_units_promo', 'sales_rub', 'sales_run_promo')
    search_fields = ('store',  'sku', 'date', 'sales_type')
    empty_value_display = '-пусто-'

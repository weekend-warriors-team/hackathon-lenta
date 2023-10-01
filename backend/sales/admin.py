from django.contrib import admin

from .models import Sale


class SaleAdmin(admin.ModelAdmin):
    """Админка продаж."""
    list_display = ('store', 'sku', 'date', 'sales_type')
    search_fields = ('store__store','sku__sku', 'date')
    list_filter = ('store', 'sku', 'date', 'sales_type')


admin.site.register(Sale, SaleAdmin)

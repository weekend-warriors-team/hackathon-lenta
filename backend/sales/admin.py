from django.contrib import admin

from .models import Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ('store', 'sku', 'date')
    search_fields = ('sku__sku',)
    list_filter = ('store', 'sku', 'date')


admin.site.register(Sale, SaleAdmin)

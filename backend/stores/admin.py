from django.contrib import admin

from .models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ('store', 'city', 'division', 'type_format', 'loc', 'size', 'is_active')
    search_fields = ('store',)
    list_filter = ('city', 'division', 'type_format', 'loc', 'size', 'is_active')


admin.site.register(Store, StoreAdmin)

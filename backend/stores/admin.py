from django.contrib import admin

from .models import City, Division, Store


class CityAdmin(admin.ModelAdmin):
    '''Админка городов'''
    list_display = ('city',)
    search_fields = ('city',)


class DivisionAdmin(admin.ModelAdmin):
    '''Админка дивизионов'''
    list_display = ('division',)
    search_fields = ('division',)


class StoreAdmin(admin.ModelAdmin):
    '''Админка магазинов'''
    list_display = (
        'store', 'city', 'division', 'type_format', 'loc', 'size', 'is_active'
    )
    search_fields = ('store',)
    list_filter = (
        'city', 'division', 'type_format', 'loc', 'size', 'is_active'
    )


admin.site.register(City, CityAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Store, StoreAdmin)

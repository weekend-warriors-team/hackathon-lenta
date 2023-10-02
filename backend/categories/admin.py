from django.contrib import admin

from .models import Category, Group, Product, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    '''Админка категорий'''
    list_display = ('title', 'group')
    search_fields = ('title',)
    list_filter = ('group',)


class GroupAdmin(admin.ModelAdmin):
    '''Админка групп'''
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


class ProductAdmin(admin.ModelAdmin):
    '''Админка продуктов'''
    list_display = ('sku', 'subcategory', 'uom')
    search_fields = ('sku',)
    list_filter = ('subcategory', 'uom')


class SubcategoryAdmin(admin.ModelAdmin):
    '''Админка подкатегорий'''
    list_display = ('title', 'category')
    search_fields = ('title',)
    list_filter = ('category',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

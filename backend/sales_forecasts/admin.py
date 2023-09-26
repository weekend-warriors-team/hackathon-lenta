from django.contrib import admin

from .models import Category, Group, Product, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku',)
    search_fields = ('sku',)
    list_filter = ('sku',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

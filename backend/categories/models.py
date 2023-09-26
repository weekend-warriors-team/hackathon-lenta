from django.db import models


class Group(models.Model):
    '''Модель группы товарной иерархии'''
    group = models.CharField(
        max_length=75
    )

    class Meta:
        verbose_name='Группа'
        verbose_name_plural='Группы'
        ordering=('group',)

    def __str__(self):
        return self.group
    

class Category(models.Model):
    '''Модель категории'''
    sku = models.CharField(max_length=75)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=75
    )
    subcategory = models.CharField(max_length=75)
    uom = models.IntegerField()

    class Meta:
        ordering = (
            'sku',
            'group',
            'category',
            'subcategory',
            'uom',
        )

    def __str__(self):
        return self.sku


class Subcategory(models.Model):
    '''Модель подкатегорий'''
    subcategory = models.CharField(max_length=75,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Подкатегория'
        verbose_name_plural='Подкатегории'

    def __str__(self):
        return self.subcategory

from django.db import models


class City(models.Model):
    '''Класс городов.'''
    city = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('city',)

    def __str__(self):
        return self.city


class Division(models.Model):
    '''Класс отделов магазинов.'''
    division = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ('division',)

    def __str__(self):
        return self.division


# class Type_format(models.Model):
#     '''Класс магазинов.'''
#     type_format = models.SmallIntegerField(unique=True)
# 
#     class Meta:
#         verbose_name = 'Формат магазина'
#         verbose_name_plural = 'Форматы магазинов'
#         ordering = ('type_format',)
# 
#     def __str__(self):
#         return self.type_format
# 
# 
# class Location(models.Model):
#     '''Класс локации.'''
#     loc = models.SmallIntegerField(unique=True)
# 
#     class Meta:
#         verbose_name = 'Локация магазина'
#         verbose_name_plural = 'Локации магазинов'
#         ordering = ('loc',)
# 
#     def __str__(self):
#         return self.loc
# 
# 
# class Size(models.Model):
#     """Класс размеров магазинов."""
# 
#     size = models.SmallIntegerField(unique=True, null=True)
# 
#     class Meta:
#         verbose_name = 'Размер'
#         verbose_name_plural = 'Размеры'
#         ordering = ('size',)
# 
#     def __str__(self):
#         return str(self.size)


class Store(models.Model):
    """Класс таблицы магазинов продуктовой иерархии."""

    store = models.CharField(max_length=50, unique=True)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='stores',
        to_field='city',
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='stores',
        to_field='division',
    )
    type_format = models.SmallIntegerField()
    loc = models.SmallIntegerField()
    size = models.SmallIntegerField(null=True)
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('store',)

    def __str__(self):
        return str(self.store)

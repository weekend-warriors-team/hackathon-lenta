from django.db import models


class Stores(models.Model):
    '''Класс магазинов'''
    store = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Магазин',
        verbose_name_plural = 'Магазины',
        ordering = ('store',)

    def __str__(self):
        return self.store


class City(models.Model):
    '''Класс городов'''
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('city',)

    def __str__(self):
        return self.city


class Division(models.Model):
    '''Класс отделов магазинов'''
    division = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ('division',)

    def __str__(self):
        return self.division


class Type_format(models.Model):
    '''Класс магазинов'''
    type_format = models.IntegerField()

    class Meta:
        verbose_name = 'Формат магазина'
        verbose_name_plural = 'Форматы магазинов'
        ordering = ('type_format',)

    def __str__(self):
        return self.type_format


class Location(models.Model):
    '''Класс локации'''
    loc = models.IntegerField()

    class Meta:
        verbose_name = 'Локация магазина'
        verbose_name_plural = 'Локации магазинов'
        ordering = ('loc',)

    def __str__(self):
        return self.loc


class Size(models.Model):
    """Класс размеров магазинов."""

    size = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ('size',)

    def __str__(self):
        return str(self.size)


class Store(models.Model):
    """Класс таблицы магазинов продуктовой иерархии."""

    store = models.ForeignKey(
        Stores,
        on_delete=models.CASCADE,
        related_name='stores',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
    )
    type_format = models.ForeignKey(
        Type_format,
        on_delete=models.CASCADE,
    )
    loc = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Таблица магазина'
        verbose_name_plural = 'Таблица магазинов'
        ordering = ('store',)

    def __str__(self):
        return str(self.store)

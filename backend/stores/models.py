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
    size = models.SmallIntegerField()
    is_active = models.BooleanField(null=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ('store',)

    def __str__(self):
        return str(self.store)

from categories.models import Product
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from stores.models import Store


class Forecast(models.Model):
    """Модель данных прогноза продаж."""
    forecast_date = models.DateField(
        verbose_name='Дата прогноза',
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name='Магазин',
        related_name='forecasts',
        to_field='store',
        default=None,
    )
    sku = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='forecasts',
        to_field='sku',
        default=None,
    )
    date = models.DateField(
        verbose_name='Дата прогнозируемой продажи',
        default=timezone.now().date(),
    )
    target = models.PositiveIntegerField(
        verbose_name='Прогнозируемый спрос',
        default=0,
    )

    class Meta:
        verbose_name = 'Прогноз продажи продукта'
        verbose_name_plural = 'Прогнозы продаж'

    def __str__(self):
        return f'{self.store}-{self.sku}-{self.date}'

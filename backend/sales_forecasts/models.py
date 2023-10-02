from categories.models import Product
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from stores.models import Store


class Forecast(models.Model):
    '''Модель данных прогноза магазина.'''
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name='Магазин',
        related_name='forecasts',
        to_field='store',
    )
    forecast_date = models.DateField(
        verbose_name='Дата прогноза'
    )

    def clean(self):
        if self.forecast_date < timezone.now().date():
            raise ValidationError(
                'Дата прогноза не может быть в прошлом'
                )

    class Meta:
        verbose_name = 'Прогноз магазина'
        verbose_name_plural = 'Прогнозы магазинов'

    def __str__(self):
        return f'{self.store}-{self.forecast_date}'


class ForecastSku(models.Model):
    '''Модель прогноза товара.'''
    forecast = models.ForeignKey(
        Forecast,
        on_delete=models.CASCADE,
        verbose_name='Прогноз магазина',
        related_name='forecasts_sku',
    )
    sku = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='forecasts_sku',
        to_field='sku',
    )

    class Meta:
        verbose_name = 'Прогноз товара'
        verbose_name_plural = 'Прогнозы товара'

    def __str__(self):
        return f'{self.forecast}-{self.sku}'


class ForecastDaily(models.Model):
    '''Модель ежедневного прогноза.'''
    sales_units = models.ForeignKey(
        ForecastSku,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='forecasts_daily',
    )
    date = models.DateField(verbose_name='Дата')
    target = models.PositiveIntegerField(verbose_name='Спрос(шт)')

    class Meta:
        verbose_name = 'Ежедневный прогноз на товар в ТЦ'
        verbose_name_plural = 'Ежедневные прогнозы на товары в ТЦ'

    def __str__(self):
        return f'{self.sales_units}-{self.sales_units.sku}-{self.date}-{self.target}'

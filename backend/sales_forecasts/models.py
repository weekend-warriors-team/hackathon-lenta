from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from stores.models import Store
from categories.models import Category


class Forecast(models.Model):
    '''Модель данных прогноза'''
    store = models.ForeignKey(Store,
                              on_delete=models.CASCADE
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
        verbose_name='Прогноз магазина'
        verbose_name_plural='Прогнозы магазинов'

    def __str__(self):
        return f'{self.store}-{self.forecast_date}'
    

class ForecastSku(models.Model):
    '''Модель прогноза товара'''
    forecast = models.ForeignKey(Forecast,
                                 on_delete=models.CASCADE
                                 )
    sku = models.ForeignKey(Category,
                            on_delete=models.CASCADE
                            )
    
    class Meta:
        verbose_name='Прогноз товара'
        verbose_name_plural='Прогнозы товара'


class ForecastDaily(models.Model):
    '''Модель ежедневного прогноза'''
    sales_units = models.ForeignKey(ForecastSku,
                                    on_delete=models.CASCADE
                                    )
    date = models.DateField(verbose_name='Дата')
    target = models.PositiveIntegerField(verbose_name='Спрос(шт)')

    class Meta:
        verbose_name='Ежедневный прогноз'
        verbose_name_plural='Ежедневные прогнозы'

    def __str__(self):
        return f'{self.sales_units}-{self.sales_units.sku}-{self.date}-{self.target}'

from django.db import models

from stores.models import Stores
from categories.models import Category


class Sales(models.Model):
    '''Модель продажи'''
    store = models.ForeignKey(Stores,
                              on_delete=models.CASCADE
                              )
    sku = models.ForeignKey(Category,
                            on_delete=models.CASCADE)

    class Meta:
        verbose_name='Продажа'
        verbose_name_plural='Продажи'

    def __str__(self):
        return f'{self.store} - {self.sku}'
    

class SalesRecord(models.Model):
    '''Модель записи продаж'''
    fact = models.ForeignKey(Sales,
                             on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    sales_type = models.IntegerField(
        verbose_name='Тип продаж'
        )
    sales_units = models.IntegerField(
        verbose_name='Число проданных товаров'
        )
    sales_units_promo = models.IntegerField(
        verbose_name='Число проданных промо товаров'
        )
    sales_rub = models.DecimalField(max_digits=10, decimal_places=2,
                                    verbose_name='Продажи в рублях'
                                    )
    sales_rub_promo = models.DecimalField(max_digits=10, decimal_places=2,
                                          verbose_name='Промо продажи в рублях'
                                          )

    class Meta:
        verbose_name='Запись продаж'
        verbose_name_plural='Записи продаж'

    def __str__(self):
        return f'{self.fact}-{self.date}'

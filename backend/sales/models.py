from categories.models import Category, Product
from django.db import models
from stores.models import Store


class Sale(models.Model):
    """Модель продаж товара в магазине за день."""

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        verbose_name='Магазин',
        related_name='sales',
        to_field='store',
        )
    sku = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='sales',
        to_field='sku',
    )
    date = models.DateField(verbose_name='Дата')
    sales_type = models.BooleanField(verbose_name='Флаг наличия промо')
    sales_units = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='Число проданных товаров без промо'
    )
    sales_units_promo = models.DecimalField(
        max_digits=12, decimal_places=3,
        verbose_name='Число проданных товаров с промо'
    )
    sales_rub = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Продажи в рублях'
    )
    sales_rub_promo = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Промо продажи в рублях'
    )

    class Meta:
        verbose_name = 'Продажа товара за день'
        verbose_name_plural = 'Продажи товаров за день'

    def __str__(self):
        return f'{self.store}-{self.sku}-{self.date}'

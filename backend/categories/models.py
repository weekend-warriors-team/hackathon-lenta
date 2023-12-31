from django.db import models


class Group(models.Model):
    """Модель группы товаров."""
    title = models.CharField(
        max_length=75, verbose_name='Название группы', unique=True
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Category(models.Model):
    """Модель категории товаров."""
    title = models.CharField(
        max_length=75, verbose_name='Название категории', unique=True
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.CASCADE,
        related_name='categories',
        to_field='title',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    """Модель подкатегории товаров."""
    title = models.CharField(
        max_length=75, verbose_name='Название подкатегории', unique=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='subcategories',
        to_field='title',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель продуктов."""
    sku = models.CharField(
        max_length=75, verbose_name='Название продукта', unique=True
    )
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        to_field='title',
    )
    uom = models.SmallIntegerField(
        verbose_name='Маркер единицы измерения',
        default=1,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['sku']

    def __str__(self):
        return self.sku

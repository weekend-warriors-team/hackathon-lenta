# Generated by Django 4.2.5 on 2023-10-01 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sales_type', models.BooleanField(verbose_name='Флаг наличия промо')),
                ('sales_units', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Число проданных продуктов без промо')),
                ('sales_units_promo', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Число проданных продуктов с промо')),
                ('sales_rub', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Продажи в рублях')),
                ('sales_rub_promo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Промо продажи в рублях')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='categories.product', to_field='sku', verbose_name='Продукт')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='stores.store', to_field='store', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Продажа продукта',
                'verbose_name_plural': 'Продажи продуктов',
            },
        ),
    ]

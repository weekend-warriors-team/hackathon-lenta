# Generated by Django 4.2.5 on 2023-10-05 12:56

import datetime
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
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField(verbose_name='Дата прогноза')),
                ('date', models.DateField(default=datetime.date(2023, 10, 5), verbose_name='Дата прогнозируемой продажи')),
                ('target', models.PositiveIntegerField(default=0, verbose_name='Прогнозируемый спрос')),
                ('sku', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='categories.product', to_field='sku', verbose_name='Продукт')),
                ('store', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='stores.store', to_field='store', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Прогноз продажи продукта',
                'verbose_name_plural': 'Прогнозы продаж',
            },
        ),
    ]

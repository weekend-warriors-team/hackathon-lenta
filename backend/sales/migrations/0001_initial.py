# Generated by Django 4.2.5 on 2023-09-29 07:38

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
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.stores')),
            ],
            options={
                'verbose_name': 'Продажа',
                'verbose_name_plural': 'Продажи',
            },
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('sales_type', models.IntegerField(verbose_name='Тип продаж')),
                ('sales_units', models.IntegerField(verbose_name='Число проданных товаров')),
                ('sales_units_promo', models.IntegerField(verbose_name='Число проданных промо товаров')),
                ('sales_rub', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Продажи в рублях')),
                ('sales_rub_promo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Промо продажи в рублях')),
                ('fact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sales')),
            ],
            options={
                'verbose_name': 'Запись продаж',
                'verbose_name_plural': 'Записи продаж',
            },
        ),
    ]

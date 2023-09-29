# Generated by Django 4.2.5 on 2023-09-29 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('city',),
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
                'ordering': ('division',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Локация магазина',
                'verbose_name_plural': 'Локации магазинов',
                'ordering': ('loc',),
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ('size',),
            },
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': ('Магазин',),
                'verbose_name_plural': ('Магазины',),
                'ordering': ('store',),
            },
        ),
        migrations.CreateModel(
            name='Type_format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_format', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Формат магазина',
                'verbose_name_plural': 'Форматы магазинов',
                'ordering': ('type_format',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.city')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.division')),
                ('loc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.location')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.size')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='stores.stores')),
                ('type_format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.type_format')),
            ],
            options={
                'verbose_name': 'Таблица магазина',
                'verbose_name_plural': 'Таблица магазинов',
                'ordering': ('store',),
            },
        ),
    ]

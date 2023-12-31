# Generated by Django 4.2.5 on 2023-10-05 12:56

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
                ('city', models.CharField(max_length=50, unique=True)),
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
                ('division', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
                'ordering': ('division',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=50, unique=True)),
                ('type_format', models.SmallIntegerField()),
                ('loc', models.SmallIntegerField()),
                ('size', models.SmallIntegerField(null=True)),
                ('is_active', models.BooleanField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='stores.city', to_field='city')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='stores.division', to_field='division')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('store',),
            },
        ),
    ]

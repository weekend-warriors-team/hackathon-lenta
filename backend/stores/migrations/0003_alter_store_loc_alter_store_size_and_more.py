# Generated by Django 4.2.5 on 2023-09-30 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_alter_store_options_alter_city_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='loc',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='store',
            name='size',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='type_format',
            field=models.SmallIntegerField(),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.DeleteModel(
            name='Type_format',
        ),
    ]

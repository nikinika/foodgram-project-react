# Generated by Django 3.2.18 on 2023-04-29 18:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_rename_measurment_unit_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredrecipe',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
    ]

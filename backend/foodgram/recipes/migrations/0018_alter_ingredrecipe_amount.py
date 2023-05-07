# Generated by Django 3.2.18 on 2023-05-07 12:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredrecipe',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]

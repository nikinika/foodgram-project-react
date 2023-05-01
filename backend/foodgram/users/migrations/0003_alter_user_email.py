# Generated by Django 3.2.18 on 2023-04-25 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_auto_20230423_2301"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
    ]

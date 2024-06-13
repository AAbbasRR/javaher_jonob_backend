# Generated by Django 5.0.4 on 2024-06-13 22:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_driver", "0001_initial"),
        ("app_factor", "0008_factor_driver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="factor",
            name="driver",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="driver_factors",
                to="app_driver.driver",
                verbose_name="Driver",
            ),
        ),
    ]

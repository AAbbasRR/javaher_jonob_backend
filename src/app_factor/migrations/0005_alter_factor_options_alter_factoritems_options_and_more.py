# Generated by Django 5.0.4 on 2024-06-26 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_factor", "0004_alter_factor_options_alter_factoritems_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="factor",
            options={"ordering": ["-create_at"]},
        ),
        migrations.AlterModelOptions(
            name="factoritems",
            options={"ordering": ["-create_at"]},
        ),
        migrations.AlterModelOptions(
            name="factorpayments",
            options={"ordering": ["-create_at"]},
        ),
    ]

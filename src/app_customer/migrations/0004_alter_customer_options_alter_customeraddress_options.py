# Generated by Django 5.0.4 on 2024-06-01 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_customer", "0003_customeraddress_city_customeraddress_street_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={"ordering": ["-create_at"]},
        ),
        migrations.AlterModelOptions(
            name="customeraddress",
            options={"ordering": ["-create_at"]},
        ),
    ]
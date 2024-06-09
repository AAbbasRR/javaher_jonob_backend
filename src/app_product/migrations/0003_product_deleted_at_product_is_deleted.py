# Generated by Django 5.0.4 on 2024-06-09 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_product", "0002_alter_product_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Deleted Time"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="is_deleted",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="Is Deleted"
            ),
        ),
    ]

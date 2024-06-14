# Generated by Django 5.0.4 on 2024-06-14 21:19

import django.core.validators
import utils.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="پاک شده"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ پاک شدن"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=32, unique=True, verbose_name="Name"),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        help_text="Unit Of Measurement is Kg",
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Weight",
                    ),
                ),
                (
                    "price",
                    utils.db.fields.PriceField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Price",
                    ),
                ),
                (
                    "tax",
                    utils.db.fields.PercentField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Tax",
                    ),
                ),
            ],
            options={
                "ordering": ["-create_at"],
                "abstract": False,
            },
        ),
    ]

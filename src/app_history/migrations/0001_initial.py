# Generated by Django 5.0.4 on 2024-06-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
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
                    "model_name",
                    models.CharField(max_length=100, verbose_name="Model Name"),
                ),
                ("object_id", models.PositiveIntegerField(verbose_name="Object Id")),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("create", "Create"),
                            ("update", "Update"),
                            ("delete", "Delete"),
                        ],
                        default="update",
                        max_length=10,
                        verbose_name="Time",
                    ),
                ),
                ("time", models.DateTimeField(auto_now_add=True, verbose_name="Time")),
                (
                    "data_before",
                    models.JSONField(blank=True, null=True, verbose_name="Data Before"),
                ),
                (
                    "data_after",
                    models.JSONField(blank=True, null=True, verbose_name="Data After"),
                ),
            ],
        ),
    ]

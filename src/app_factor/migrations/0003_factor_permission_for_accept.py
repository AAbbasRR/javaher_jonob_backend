# Generated by Django 5.0.4 on 2024-05-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_factor", "0002_alter_factor_is_accepted"),
    ]

    operations = [
        migrations.AddField(
            model_name="factor",
            name="permission_for_accept",
            field=models.CharField(
                choices=[
                    ("superuser_staff", "Superuser Or Staff"),
                    ("secretary_superuser_staff", "Secretary Or Superuser Or Staff"),
                ],
                default="secretary_superuser_staff",
                max_length=25,
                verbose_name="Permission For Accept",
            ),
        ),
    ]

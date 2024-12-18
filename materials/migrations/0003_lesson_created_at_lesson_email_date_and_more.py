# Generated by Django 5.1.3 on 2024-11-28 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Дата создания"
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="email_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата сообщения об изменении"
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата последнего изменения"
            ),
        ),
    ]

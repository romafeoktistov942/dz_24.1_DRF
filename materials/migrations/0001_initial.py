# Generated by Django 5.1.3 on 2024-11-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                    "course_name",
                    models.CharField(
                        help_text="Введите название курса",
                        max_length=30,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите фото",
                        null=True,
                        upload_to="materials/preview",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Заполните описание",
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                    "lesson_name",
                    models.CharField(
                        help_text="Введите название урока",
                        max_length=30,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Заполните описание",
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите фото",
                        null=True,
                        upload_to="materials/preview",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "video",
                    models.CharField(
                        blank=True,
                        help_text="Загрузите видео",
                        max_length=500,
                        null=True,
                        verbose_name="Ссылка на видео",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]

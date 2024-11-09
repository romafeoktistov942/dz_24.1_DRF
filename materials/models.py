from django.db import models

from config import settings


class Course(models.Model):
    course_name = models.CharField(
        max_length=30,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Заполните описание",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Создатель курса",
        help_text="Укажите создателя курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.course_name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    lesson_name = models.CharField(
        max_length=30,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Заполните описание",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
        null=True,
    )
    video = models.CharField(
        max_length=500,
        verbose_name="Ссылка на видео",
        help_text="Загрузите видео",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        help_text="Укажите курс",
        verbose_name="Курс",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Создатель урока",
        help_text="Укажите создателя урока",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.course_name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

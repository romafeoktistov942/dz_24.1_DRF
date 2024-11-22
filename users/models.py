from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.CharField(
        max_length=150,
        verbose_name="Почта",
        help_text="Введите почту",
        unique=True,
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Укажите страну",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.email}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = "Cash"
    NON_CASH = "Non_cash"
    PAYMENT_METHOD_CHOICES = [
        (CASH, "Наличные"),
        (NON_CASH, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        blank=True,
        null=True,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        help_text="Укажите урок",
        blank=True,
        null=True,
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
        blank=True,
        null=True,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        blank=True,
        null=True,
    )
    payment_date = models.DateField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"


class Subscription(models.Model):
    """Класс модели подписка на курс"""

    subscription_name = models.CharField(
        max_length=100,
        verbose_name="Подписка",
        help_text="Укажите название подписки",
        default="Подписка",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь подписки",
        help_text="Укажите пользователя подписки",
        related_name="subsuser",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Подписка на курс",
        help_text="Укажите курс подписки",
        related_name="subscourse",
    )
    subscription_sign = models.BooleanField(
        default=False, verbose_name="Признак подписки"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} : {self.course}"

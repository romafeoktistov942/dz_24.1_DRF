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
    """Модель оплаты"""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        blank=True,
        null=True,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Укажите курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
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
        choices={"Cash": "Наличные", "Non_cash": "Перевод на счет"},
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        blank=True,
        null=True,
    )
    payment_date = models.DateField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
    )
    link = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Ссылка для оплаты",
        help_text="Укажите ссылку для оплаты",
    )
    status_pay = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Статус оплаты",
        help_text="Укажите статус оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.payment_amount}"


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

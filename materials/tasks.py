import smtplib
from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from materials.models import Lesson
from users.models import User


@shared_task
def send_change_subs(data_name, email_list):
    """
    Уведомляет об изменении подписки.
    """
    print("Отправка сообщения об изменении подписки")
    try:
        send_mail(
            subject=f"Изменения в: {data_name}",
            message="Сообщаем Вам, в подписке произошли изменения",
            from_email=EMAIL_HOST_USER,
            recipient_list=email_list,
        )
    except smtplib.SMTPException as server_response:
        print(server_response)


@shared_task
def check_last_login():
    """
    Деактивирует неактивных пользователей.
    """
    print("Проверка last_login")
    current_date = now()
    users = User.objects.all()
    for user in users:
        print(user.last_login)
        if user.last_login:
            if user.last_login < current_date - timedelta(days=30):
                user.is_active = False
        else:
            if user.date_joined < current_date - timedelta(days=30):
                user.is_active = False
        user.save()


@shared_task
def check_update_lesson():
    """Отправляем уведомления об изменениях в уроках, произошедших за последние 4 часа"""
    print("Проверяем наличие изменений за последние 4 часа")
    date = now()
    lesson = Lesson.objects.all()
    email_list = []
    for les in lesson:
        if les.email_date and les.updated_ta:
            if date > les.email_date + timedelta(
                hours=4
            ) and date > les.updated_ta + timedelta(hours=4):
                les.email_date = date
                email_list.append(les.owner.email)
    if email_list:
        try:
            send_mail(
                subject=f"Обновления в уроке '{lesson[0].lesson_name}'",
                message=f"Пожалуйста, ознакомьтесь с изменениями в уроке: {lesson[0].description}",
                from_email=EMAIL_HOST_USER,
                recipient_list=email_list,
            )
        except smtplib.SMTPException as server_response:
            print(server_response)

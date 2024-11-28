from users.models import Subscription


def get_subs_changes(course):
    """Возвращает список подписчиков курса, у которых изменилось содержание"""
    return get_set(course)


def get_lesson_changes(lesson):
    """Возвращает список подписчиков урока, у которых изменилось содержание"""
    course = lesson.course
    return get_set(course)


def get_set(data):
    """Формирует список адресов электронной почты подписчиков"""
    subscription = Subscription.objects.filter(course=data)
    email_list = []
    for subs in subscription:
        email_list.append(subs.user.email)
    return email_list

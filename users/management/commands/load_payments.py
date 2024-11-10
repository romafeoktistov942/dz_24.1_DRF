from django.core.management.base import BaseCommand
from users.models import Payments, User
from materials.models import Course, Lesson

class Command(BaseCommand):
    help = 'Загрузить данные платежей'

    def handle(self, *args, **options):
        payments = [
            {'user': User.objects.get(id=2), 'payment_date': '2022-01-01', 'paid_course': Course.objects.get(id=2), 'paid_lesson': None, 'payment_amount': 100.00, 'payment_method': 'Cash'},
            {'user': User.objects.get(id=3), 'payment_date': '2022-01-15', 'paid_course': None, 'paid_lesson': Lesson.objects.get(id=3), 'payment_amount': 50.00, 'payment_method': 'Non_cash'},
        ]

        for payment in payments:
            Payments.objects.create(**payment)

        self.stdout.write(self.style.SUCCESS('Данные платежей загружены успешно'))
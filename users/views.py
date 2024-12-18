from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from materials.models import Course
from users.permissions import IsOwner
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)
from .serializers import (
    PaymentsSerializer,
    SubscriptionSerializer,
    UserSerializer,
)

# from users.services import convert_rub_to_usd
from .models import Payments, User, Subscription
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Проверяем, если подписка у пользователя есть, то удаляем.
        Если подписки нет, то добавляем
        """
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item, subscription_sign=True
            )
            message = "Подписка создана"

        return Response({"message": message})


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class PaymentsCreateAPIView(CreateAPIView):
    """
    Создание платежа
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course = Course.objects.get(pk=payment.paid_course_id)
        # amount = convert_rub_to_usd(payment.payment_amount)
        product = create_stripe_product(course)
        price = create_stripe_price(payment.payment_amount, product)
        session_id, payment_link = create_stripe_session(product, price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

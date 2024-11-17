from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PaymentsSerializer, UserSerializer
from .models import Payments, User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


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
        print("POST-запрос получен")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("Сериализатор вызван")
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

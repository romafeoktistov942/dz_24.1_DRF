from users.apps import UsersConfig
from users import views

from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from .views import PaymentsViewSet, UserCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path

app_name = UsersConfig.name

router = DefaultRouter()
router.register("payments", PaymentsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

from users.apps import UsersConfig
from users import views

from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionViewSet,
    UserViewSet,
    PaymentsViewSet,
    SubscriptionUpdateAPIView,
    UserCreateAPIView,
    SubscriptionListAPIView,
    SubscriptionCreateAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentsViewSet)
router.register(r"subscriptions", SubscriptionViewSet, basename="subscriptions")

urlpatterns = [
    path("api/", include(router.urls)),
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
    path(
        "subscription/list/",
        SubscriptionListAPIView.as_view(),
        name="subscription-list",
    ),
    path(
        "subscription/create/",
        SubscriptionCreateAPIView.as_view(),
        name="subscription-create",
    ),
    path(
        "subscription/update/<int:pk>/",
        SubscriptionUpdateAPIView.as_view(),
        name="subscription-update",
    ),
]

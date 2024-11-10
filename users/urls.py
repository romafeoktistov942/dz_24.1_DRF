from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from .views import PaymentsViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register("payments", PaymentsViewSet)

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseUpdateAPIView,
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonDestroyAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path(
        "lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"
    ),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_retrieve",
    ),
    path(
        "lessons/<int:pk>/update/",
        LessonUpdateAPIView.as_view(),
        name="lesson_update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lesson_delete",
    ),
    path(
        "course/update/<int:pk>",
        CourseUpdateAPIView.as_view(),
        name="course-update",
    ),
]

urlpatterns += router.urls

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    LessonDetailSerializer,
)
from materials.services import get_lesson_changes, get_subs_changes
from materials.tasks import send_change_subs
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModer | IsOwner]
        return super().get_permissions()


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def get_queryset(self):
        """Получаем список подписчиков курса"""
        course_id = self.kwargs.get("pk")
        course = Course.objects.get(pk=course_id)
        email_list = get_subs_changes(course)
        send_change_subs.delay(course.course_name, email_list)
        return super().get_queryset()


class LessonCreateAPIView(CreateAPIView):
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]

    def get_queryset(self):
        """Проверяем последнее изменения Урока"""
        lesson_id = self.kwargs.get("pk")
        lesson = Lesson.objects.get(pk=lesson_id)
        email_list = get_lesson_changes(lesson)
        send_change_subs.delay(lesson.lesson_name, email_list)
        return super().get_queryset()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]

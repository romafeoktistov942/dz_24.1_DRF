from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_allowed_words
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validate_allowed_words])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    def get_lessons(self, course):
        return LessonSerializer(
            Lesson.objects.filter(course=course.pk).order_by("pk"), many=True
        ).data

    def get_subscription(self, course):
        user = self.context["request"].user
        subscription = Subscription.objects.filter(
            user=user, course=course
        ).first()
        if subscription:
            return {"id": subscription.id}
        else:
            return None

    class Meta:
        model = Course
        fields = (
            "id",
            "course_name",
            "preview",
            "description",
            "owner",
            "lessons_count",
            "lessons",
            "subscription",
        )


class LessonDetailSerializer(serializers.ModelSerializer):
    count_lesson_with_same_course = serializers.SerializerMethodField()
    course = CourseSerializer(read_only=True)

    def get_count_lesson_with_same_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "description",
            "preview",
            "video",
            "course",
            "count_lesson_with_same_course",
        )

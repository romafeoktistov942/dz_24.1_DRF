from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_allowed_words


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validate_allowed_words])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    def get_lessons(self, course):
        return LessonSerializer(
            Lesson.objects.filter(course=course.pk).order_by("pk"), many=True
        ).data

    class Meta:
        model = Course
        fields = (
            "course_name",
            "preview",
            "description",
            "owner",
            "lessons_count",
            "lessons",
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

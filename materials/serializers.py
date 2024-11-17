from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()

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


class LessonDetailSerializer(ModelSerializer):
    count_lesson_with_same_course = SerializerMethodField()
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

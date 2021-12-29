from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from course.models import Lecture, Course


class LectureSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(read_only=True)
    name_course = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Lecture.objects.all())])

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'file_present', 'published_at', 'professor', 'name_course']



class CourseLectureSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name_course', 'lectures']

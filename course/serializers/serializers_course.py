from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from course.models import Course, StudCour, TeachCour

MyUser = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    name_course = serializers.CharField(max_length=125, validators=[UniqueValidator(queryset=Course.objects.all())])

    class Meta:
        model = Course
        fields = ['id', 'name_course', 'description', 'published_at', 'update_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name_course', 'description', 'published_at', 'update_at', 'author']


#
#
# class StudCourSerializer(serializers.ModelSerializer):
#     course = CourseSerializer()
#
#     class Meta:
#         model = StudCour
#         fields = ['id', 'student', 'course']
#
#
# class TeachAddSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeachCour
#         fields = ['teacher', 'course']


# class CoursesProfessorsSerializer(serializers.ModelSerializer):
#     teacher = UserSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Course
#         fields = ['teacher']


class AddTeacherSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(AddTeacherSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if not request:
            return
        self.fields["teacher"] = serializers.ChoiceField(
            choices=[i.username for i in MyUser.objects.filter(status='p')])

    class Meta:
        fields = ['teacher']
#
#
class AddStudentSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(AddStudentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if not request:
            return
        self.fields["student"] = serializers.ChoiceField(
            choices=[i.username for i in MyUser.objects.filter(status='s')])

    class Meta:
        fields = ['student']

from django.contrib.auth import get_user_model
from rest_framework import serializers

from course.models import MessageTeacher, Mark, Solution, Homework, MessageStudent
from course.serializers.serializers_solutions import SolutionSerializers

MyUser = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTeacher
        fields = ['id', 'text', 'published_at']


class MarkSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(MarkSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if not request:
            return
        self.fields["solution_id"] = serializers.ChoiceField(
            choices=[i.id for i in Solution.objects.all()])

    # solution_id = serializers.ChoiceField(choices=[i.id for i in Solution.objects.all()])
    mark = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Mark
        fields = ['mark', 'solution_id', 'text_message_teacher']

    def validate(self, data):
        solution_id = self.context['request'].data['solution_id']
        if Mark.objects.filter(solution_id=solution_id).count() > 0:
            raise serializers.ValidationError("Вы добавили оценку")
        return data


# _______________________________________________________________________________________________
# class SolutionForProfessorCheckSerializer(serializers.ModelSerializer):
#     id_user = serializers.IntegerField(source='id', read_only=True)
#     user_solution = SolutionSerializers(many=True)
#
#     class Meta:
#         model = MyUser
#         fields = ['id_user', 'username', 'user_solution', ]


# _______________________________________________________________________________________________
class MarkDetailSerializers(serializers.ModelSerializer):
    solution = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Mark
        fields = ['mark', 'solution', 'text_message_teacher']


# ____________________SolutionForCheckProfessorSerializer______________________________________
class MarkToProfessorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'mark']


class UserToSolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    id_user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = MyUser
        fields = ['id_user', 'username']


class HSToSolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'title']


class SolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    user_solution = UserToSolutionForCheckProfessorSerializer()
    homework_solution = HSToSolutionForCheckProfessorSerializer()
    mark_solution = MarkToProfessorSerializers()

    class Meta:
        model = Solution
        fields = ['id', 'solution_task', 'user_solution', 'homework_solution', 'mark_solution']


# ____________________StudentLookSolutionSerializers_______________________________________
class MarkToStudentSerializers(serializers.ModelSerializer):
    mark_message = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Mark
        fields = ['mark', 'mark_message']


class StudentLookHisSolutionSerializers(serializers.ModelSerializer):
    mark_solution = MarkToStudentSerializers()
    message_solution_teachers = MessageSerializer(many=True)

    class Meta:
        model = Solution
        fields = ['id', 'solution_task', 'mark_solution', 'message_solution_teachers']


# ___________________StudentMessage___________________________________________________________

class StudentMessageSerializers(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(StudentMessageSerializers, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if not request:
            return
        user = self.context["request"].user
        self.fields["message_solution_students_id"] = serializers.ChoiceField(
            choices=[i.id for i in Solution.objects.filter(user_solution_id=user.pk)])

    class Meta:
        model = MessageStudent
        fields = ['id', 'text', 'published_at', 'message_solution_students_id']


# _________________________________ListMessageForProfessor_______________________________________

class MessageStudentSerialezers(serializers.ModelSerializer):
    class Meta:
        model = MessageStudent
        fields = ['text', 'published_at']


class ListMessageForProfessorSerialezers(serializers.ModelSerializer):
    message_solution_students = MessageStudentSerialezers(many=True)

    class Meta:
        model = Solution
        fields = ['id', 'solution_task', 'mark_solution', 'message_solution_students']

from rest_framework import serializers

from course.models import Solution, Homework
from course.serializers.serializers_lecture import LectureSerializer


class SolutionSerializers(serializers.ModelSerializer):
    task_solved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Solution
        fields = ['id', 'task_solved', 'solution_task', 'homework_solution']

    def validate(self, data):
        user_id = self.context['request'].user.pk

        homework_id = self.context['request'].data['homework_solution']
        if Solution.objects.filter(user_solution_id=user_id, homework_solution_id=homework_id).count() > 0:
            raise serializers.ValidationError("Вы добавили уже решение")
        return data


class HomeworkForSolution(serializers.ModelSerializer):
    lecture_for_homework = LectureSerializer()

    class Meta:
        model = Homework
        fields = ['id', 'title', 'homework_task', 'lecture_for_homework']

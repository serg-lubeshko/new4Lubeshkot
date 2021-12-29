from rest_framework import serializers

from course.models import Lecture, Homework
from course.serializers.serializers_lecture import LectureSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(read_only=True)
    # lecture_for_homework = serializers.ChoiceField(
    #     choices=[i.id for i in Lecture.objects.all()],                #Можно лекции вывессти только свои
    #     source='lecture_for_homework_id')

    class Meta:
        model = Homework
        fields = ['id', 'title', 'homework_task', 'published_at', 'professor', 'lecture_for_homework']

    def validate(self, data):
        user_id = self.context['request'].user.pk
        lecture_id = self.context['request'].data['lecture_for_homework']
        if Homework.objects.filter(professor_id=user_id, lecture_for_homework=lecture_id).count() > 0:
            raise serializers.ValidationError("Вы добавили уже домашнюю работу")
        return data


class LectureFofHomework(LectureSerializer):
    homework = HomeworkSerializer(many=True, source='lecture_for_homework')

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'homework']

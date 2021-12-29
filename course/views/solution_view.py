from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.conf.permission import IsStudentOrReadOnly
from course.models import Homework
from course.serializers.serializers_solutions import SolutionSerializers, HomeworkForSolution


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Студент отправляет ссылку на решения по Д/з",
    operation_summary="Студент отправляет ССЫЛКУ на Solution, homework_solution => id домашней работы преподователя  "
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Студент смотрит СВОИ домашние работы",
    operation_summary="Студент смотрит СВОИ домашние работы"))
class SolutionToHomework(generics.GenericAPIView):
    """ Решения студентов """

    permission_classes = [IsAuthenticated, IsStudentOrReadOnly]
    serializer_class = SolutionSerializers
    queryset = Homework.objects.all()

    def get(self, request):
        query = Homework.objects.filter(lecture_for_homework__course__student=self.request.user)
        serializer = HomeworkForSolution(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_solution_id=self.request.user.id, task_solved=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

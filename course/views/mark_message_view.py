from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.conf.permission import IsProfessorOrReadOnlyMark, IsProfessorOrReadOnlyMarkDetail, IsStudentReadOnly
from course.models import Solution, MessageTeacher, Mark
from course.serializers.serializers_mark_message import MarkSerializer, SolutionForCheckProfessorSerializer, \
    MarkDetailSerializers, StudentLookHisSolutionSerializers, StudentMessageSerializers, \
    ListMessageForProfessorSerialezers

MyUser = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Профессор ставит оценку, пишет комментарий"))
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Профессор смотрит решения студентов. Разделил json на решения: "
                          "проверенные и не проверенные им "))
class ProfessorWatchHomework(generics.GenericAPIView):
    """ Профессор смотрит solution и ставит оценку, может написать комментарий"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMark]
    serializer_class = MarkSerializer
    queryset = MyUser.objects.all()

    def get(self, request):
        query = Solution.objects.filter(task_solved=True,
                                        homework_solution__professor_id=request.user.pk)
        checked_query = query.filter(task_cheked=True)
        unchecked_query = query.filter(task_cheked=False)
        checked_serializer = SolutionForCheckProfessorSerializer(checked_query, many=True)
        unchecked_serializer = SolutionForCheckProfessorSerializer(unchecked_query, many=True)
        return Response(({'unchecked_solution': unchecked_serializer.data},
                         {'checked_solution': checked_serializer.data},)
                        )

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_mark_id=request.user.pk)
            Solution.objects.filter(id=request.data["solution_id"]).update(task_cheked=True)
            MessageTeacher.objects.create(message_solution_teachers_id=request.data["solution_id"],
                                          text=request.data["text_message_teacher"])
            return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Профессор обновляет оценку, пишет комментарий"))
class ProfessorMarkDetail(generics.RetrieveUpdateAPIView):
    """ Профессор обновляет оценку и пишет комментарий"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMarkDetail]
    serializer_class = MarkDetailSerializers
    queryset = Mark.objects.all()
    lookup_field = 'solution_id'

    def put(self, request, *args, **kwargs):
        MessageTeacher.objects.create(message_solution_teachers_id=kwargs['solution_id'],
                                      text=request.data["text_message_teacher"])
        return self.update(request, *args, **kwargs)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Студент смотрит оценку и комментарии профессора"))
class StudentLookHisSolution(generics.GenericAPIView):
    """ Студент смотрит оценку и комментарии профессора"""

    permission_classes = [IsAuthenticated, IsStudentReadOnly]
    serializer_class = StudentLookHisSolutionSerializers

    def get(self, request):
        query = Solution.objects.filter(task_solved=True,
                                        user_solution_id=request.user.pk)
        verified_query = query.filter(task_cheked=True)
        unverified_query = query.filter(task_cheked=False)
        verified_serializer = StudentLookHisSolutionSerializers(verified_query, many=True)
        unverified_serializer = StudentLookHisSolutionSerializers(unverified_query, many=True)
        return Response(({'verified_homework': verified_serializer.data},
                         {'unverified_homework': unverified_serializer.data})
                        )


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Студент пишет комментарий к Solution"))
class StudentMessage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudentReadOnly]
    serializer_class = StudentMessageSerializers

    # def get(self, request, solution_id):
    #     query = Solution.objects.get(id=solution_id)
    #     serializer = StudentMessageGETSerializers(query)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_message_id=request.user.pk)
            return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Проффесор смотрит сообщения студента к его Solution"))
class ListMessageForProfessor(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMarkDetail]
    serializer_class = ListMessageForProfessorSerialezers

    def get_queryset(self):
        return Solution.objects.filter(task_solved=True,
                                       homework_solution__professor_id=self.request.user.pk)

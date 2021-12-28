from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from course.conf.functions_app.Check import CheckCourse
from course.conf.permission import IsProfessorOrReadOnly, IsOwnerOrReadOnly
from course.models import Course, TeachCour, StudCour

MyUser = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Профессор добавляет курс"))
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="СВОИ курсы могут смотреть только приглашенные студенты/проффесора, авторы"))
class CourseList(generics.ListCreateAPIView):
    """Список курсов для приглашенных и авторов(каждый свои курсы), а также добавление нового курса"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CourseSerializer

    def get_queryset(self):
        person = MyUser.objects.get(username=self.request.user)
        user_pk = person.pk
        user_status = person.status
        if user_status in ('p',):
            return Course.objects.filter(teacher=user_pk)
        if user_status in ('s',):
            return Course.objects.filter(student=user_pk)

    def perform_create(self, serializer):
        course_object = serializer.save(author=self.request.user)
        TeachCour.objects.create(course_id=course_object.id, teacher_id=course_object.author_id)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Указываем id_курса и смотрим инфо; по id_курсу выполняем RUD"))
class DetailCourse(generics.RetrieveUpdateDestroyAPIView):
    """ Detail могут смотреть студенты и профессора своего курса, владельцы вносить изменения """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProfessorOrReadOnly]
    serializer_class = CourseDetailSerializer

    def get_queryset(self):
        person = MyUser.objects.get(username=self.request.user)
        user_pk = person.pk
        user_status = person.status
        if user_status in ('p',):
            return Course.objects.filter(teacher=user_pk)
        if user_status in ('s',):
            return Course.objects.filter(student=user_pk)


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Добавление нового преподавателя к своему курсу"))
class AddTeacher(GenericAPIView):
    """ Добавляет профессора """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProfessorOrReadOnly]
    serializer_class = AddTeacherSerializer

    # def get(self, request, course_id):
    #     try:
    #         quer = Course.objects.get(id=course_id)
    #         serializer = CourseDetailSerializer(quer)
    #         return Response(serializer.data)
    #     except Course.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id):
        check = CheckCourse(course_id, request.data['teacher']).get_professor()
        if check is None:
            serializer = self.serializer_class(data=request.data)
            teacher_pk = MyUser.objects.filter(username=request.data['teacher'])[0].pk
            if serializer.is_valid(raise_exception=True) and teacher_pk:
                TeachCour.objects.create(course_id=course_id, teacher_id=teacher_pk)
                return Response({'message': 'Новый профессор добавлен'}, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "userMessage": check,
            },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_description="Удаление нового студента к своему курсу. "
                          "метод DELETE не позволяет ввести доп.поле на удаление"))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Добавление нового студента к своему курсу"))
class AddStudent(GenericAPIView):
    """ Добавляем/удаляем студента     """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProfessorOrReadOnly]
    serializer_class = AddStudentSerializer

    # def get(self, request, course_id):
    #     try:
    #         quer = Course.objects.get(id=course_id)
    #         serializer = CourseSerializer(quer)
    #         return Response(serializer.data)
    #     except Course.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id):
        check = CheckCourse(course_id, request.data['student']).get_student(request.user.pk)
        if check is None:
            serializer = self.serializer_class(data=request.data)
            student_pk = MyUser.objects.filter(username=request.data['student'])[0].pk
            if serializer.is_valid():
                StudCour.objects.create(course_id=course_id, student_id=student_pk)
                return Response({'message': 'Новый студент добавлен'}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "userMessage": check,
            },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def put(self, request, course_id):
        try:
            student_pk = MyUser.objects.get(username=request.data['student']).pk
            StudCour.objects.get(course_id=course_id, student_id=student_pk).delete()
        except (MyUser.DoesNotExist, StudCour.DoesNotExist):
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_204_NO_CONTENT)

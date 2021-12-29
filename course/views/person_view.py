from django.contrib.auth import logout, authenticate, login, get_user_model
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from course.serializers.serializers_person import UserSerializer, ListUsersSerializer

MyUser = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Создание профессора/студента",
    operation_summary="Создание профессора/студента"))
class UserCreate(CreateAPIView):
    """ Регистрация пользователя """

    model = MyUser
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = UserSerializer


def user_logout(request):
    logout(request)
    return redirect('/')


class MyLoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Список пользователей",
    operation_summary="Список юзеров"
))
class ListPerson(ListAPIView):
    """ Вывод списка пользователей """

    serializer_class = ListUsersSerializer
    queryset = MyUser.objects.all()

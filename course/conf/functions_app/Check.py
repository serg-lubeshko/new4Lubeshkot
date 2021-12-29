from django.contrib.auth import get_user_model

from course.conf.functions_app.get_object_or_None import get_object_or_None
from course.models import Course, TeachCour, StudCour

MyUser = get_user_model()


class CheckCourse:
    def __init__(self, course: id, username: str):
        self.course = course
        self.username = username

    def check_course(self):
        "Есть ли курс"
        return get_object_or_None(Course, pk=self.course)

    def get_professor(self, teacher_user_id):
        """  Проверка профессора добавлении на курс"""

        user = get_object_or_None(MyUser, username=self.username)

        if user is None or user.status != 'p':
            return "Такой пользователь не может быть добавлен"
        course = self.check_course()
        if course is None:
            return "Такого курса нет"
        user_id = user.pk
        if not TeachCour.objects.filter(course_id=self.course).filter(teacher_id=teacher_user_id):
            return "Другого профессора может добавить автор либо приглашенный профессор"
        if course.author_id == user_id or user.pk == teacher_user_id:
            return "На курс профессор не может быть добавлен"
        if TeachCour.objects.filter(course_id=self.course).filter(teacher_id=user_id):
            return "Профессор уже добавлен"
        return None

    def get_student(self, student_user_id):
        """  Проверка профессора студента на курс"""

        user_student = get_object_or_None(MyUser, username=self.username)
        if user_student is None or user_student.status != 's':
            return "Такой пользователь не может быть добавлен"
        course = self.check_course()
        if course is None:
            return "Такого курса нет"
        user_id_student = user_student.pk
        if course.author_id == user_id_student:
            return "Сам себя владелец не может добавить"
        if not TeachCour.objects.filter(course_id=self.course).filter(teacher_id=student_user_id):
            return "Студента может добавить автор либо приглашенный профессор"
        if StudCour.objects.filter(course_id=self.course).filter(student_id=user_id_student):
            return "Студент уже добавлен"

        # return user_student.pk, None

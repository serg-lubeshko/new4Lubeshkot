from rest_framework import permissions

from course.models import StudCour, TeachCour, Lecture, Homework


class IsStudentReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.status == 's'


class IsProfessorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.status == 'p'


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsRegisteredPersonCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        param = request.parser_context['kwargs'].get('course_id')
        status_user = request.user.status
        if status_user in 's':
            if request.method in permissions.SAFE_METHODS and StudCour.objects.filter(
                    student_id=request.user.pk).filter(course_id=param):
                return True
        if status_user in ('p',) and TeachCour.objects.filter(teacher_id=request.user.pk).filter(course_id=param):
            return True
        return False


class IsProffesorToLecture(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.professor.pk == request.user.pk


class IsLecturerOrReadOnly(permissions.BasePermission):
    message = 'Проверьте запрос, возможно такой лекции у Вас нет'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            param_solution = request.data['lecture_for_homework']
            professor_pk = Lecture.objects.get(id=param_solution).professor_id
        except Lecture.DoesNotExist:
            return False
        return bool(request.user.status == 'p' and request.user.pk == professor_pk)


class IsStudentOrReadOnly(permissions.BasePermission):
    message = "Только студент данного курса может выполнять действия"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.status == 's'
        try:
            param_solution = request.data['homework_solution']
            homework_count = Homework.objects.filter(
                lecture_for_homework__course__studcour__student_id=request.user.pk).filter(id=param_solution).count()
        except (Homework.DoesNotExist, KeyError):
            return False
        return bool(request.user.status == 's' and homework_count > 0)


class IsProfessorOrReadOnlyMark(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.status == 'p'
        try:
            param_solution = request.data['solution_id']
            professor_pk = Homework.objects.get(homework_solution__id=param_solution).professor_id
        except Homework.DoesNotExist:
            return False
        return bool(request.user.status == 'p' and request.user.pk == professor_pk)


class IsProfessorOrReadOnlyMarkDetail(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.status == 'p'
        # param_solution = request.data['solution_id']
        print(request.parser_context['kwargs'])
        try:
            param_solution = request.parser_context['kwargs'].get('solution_id')
            professor_pk = Homework.objects.get(homework_solution__id=param_solution).professor_id
        except Homework.DoesNotExist:
            return False
        return bool(request.user.status == 'p' and request.user.pk == professor_pk)


class IsRegisteredStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            param = request.parser_context['kwargs'].get('homework_id')
            id_lecture = Homework.objects.get(id=param).lecture_for_homework_id
            id_course = Lecture.objects.get(id=id_lecture).course_id
            user = request.user.pk
            return StudCour.objects.filter(course_id=id_course).filter(student_id=user)
        except Homework.DoesNotExist:
            return False


class IsRegisteredPersonHomework(permissions.BasePermission):
    def has_permission(self, request, view):
        param_lecture = request.parser_context['kwargs'].get('lecture_id')
        param = Lecture.objects.get(id=param_lecture).course_id
        status_user = request.user.status
        if status_user in 's':
            if request.method in permissions.SAFE_METHODS and StudCour.objects.filter(
                    student_id=request.user.pk).filter(course_id=param):
                return True
        if status_user in ('p',) and TeachCour.objects.filter(teacher_id=request.user.pk).filter(course_id=param):
            return True
        return False

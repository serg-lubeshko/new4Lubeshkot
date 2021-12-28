from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    """ Модель Пользователей """
    class StatusPerson(models.TextChoices):
        Pr = 'p', 'Professor'
        St = 's', 'Student'

    status = models.CharField(max_length=2,
                              verbose_name='Статус юзера',
                              choices=StatusPerson.choices,
                              default=StatusPerson.Pr)

    def __str__(self):
        return self.username


class Course(models.Model):
    """ Модель курсов """

    name_course = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание', blank=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Последние изменения')
    author = models.ForeignKey(MyUser, related_name='author_user', verbose_name='автор курса', on_delete=models.CASCADE)
    student = models.ManyToManyField(MyUser, related_name='student', verbose_name='студент курса',
                                     through='StudCour', )
    teacher = models.ManyToManyField(MyUser, related_name='teacher', verbose_name='соавтор курса',
                                     through='TeachCour', )

    def __str__(self):
        return f"{self.name_course}|{self.author}"


class StudCour(models.Model):
    """ Модель приглашенных студентов """

    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course}|{self.student}"


class TeachCour(models.Model):
    """ Модель приглашенных преподователей """

    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tea')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cou')

    def __str__(self):
        return f"{self.course}|{self.teacher}"


class Lecture(models.Model):
    """ Модель лекций """

    title = models.CharField(max_length=255, verbose_name='Название лекции')
    file_present = models.FileField(upload_to='files/%Y/%m/%d/', blank=True, verbose_name="Презентация")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    professor = models.ForeignKey(MyUser, related_name='professor', verbose_name='Автор лекции',
                                  on_delete=models.CASCADE)

    course = models.ForeignKey(Course, related_name='lectures', verbose_name='Курс', on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.title} - автор {self.professor}"


class Homework(models.Model):
    """ Модель домашних заданий """

    homework_task = models.TextField(verbose_name='Домашняя работа')
    title = models.CharField(verbose_name='Название домашней работы', max_length=155)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    professor = models.ForeignKey(MyUser, related_name='professor_lec', verbose_name='Автор лекции',
                                  on_delete=models.CASCADE)

    lecture_for_homework = models.ForeignKey(Lecture, related_name='lecture_for_homework', verbose_name='Лекция',
                                             on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.title} - автор {self.professor}"


class Solution(models.Model):
    """ Модель решения задачи """

    solution_task = models.URLField(verbose_name='Решение')
    user_solution = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_solution',
                                      verbose_name='Студент')
    homework_solution = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='homework_solution',
                                          verbose_name='Домашняя работа')
    task_solved = models.BooleanField(verbose_name='Задача решена?')
    task_cheked = models.BooleanField(verbose_name='Задача проверена?', default=0)

    def __str__(self):
        return f'{self.solution_task} - {self.homework_solution}'


class Mark(models.Model):
    """ Модель оценок """

    mark = models.SmallIntegerField(verbose_name='Оценка')
    solution = models.OneToOneField(Solution, verbose_name='Решение', related_name='mark_solution', blank=True,
                                         null=True,
                                         on_delete=models.CASCADE)
    user_mark = models.ForeignKey(MyUser, related_name='user_mark', on_delete=models.CASCADE)
    text_message_teacher = models.TextField('Сообщение профессора', blank=True, null=True)


    def __str__(self):
        return f'{self.mark} | {self.solution}'


class MessageTeacher(models.Model):
    """ Модель сообщений профессоров """

    text = models.TextField(blank=False, null=True, verbose_name='Текстовое сообщение')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    message_solution_teachers = models.ForeignKey(Solution, verbose_name='Решение_ID', on_delete=models.CASCADE,
                                     related_name='message_solution_teachers')

    def __str__(self):
        return f'Сообщение текстовое {self.text}'



class MessageStudent(models.Model):
    """ Модель сообщений студента """

    text = models.TextField(blank=False, null=True, verbose_name='Текстовое сообщение')
    message_solution_students = models.ForeignKey(Solution, verbose_name='Решение_ID', on_delete=models.CASCADE,
                                     related_name='message_solution_students')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    user_message = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_message')

    def __str__(self):
        return f'Сообщение текстовое {self.text}'
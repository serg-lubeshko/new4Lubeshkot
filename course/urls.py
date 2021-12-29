from django.urls import path

from course.views.course_view import CourseList, AddStudent, AddTeacher, DetailCourse
from course.views.homework_view import HomeworkToLecture
from course.views.lecture_view import LectureList, LectureRUD, LectureToCourse
from course.views.mark_message_view import ListMessageForProfessor, ProfessorWatchHomework, ProfessorMarkDetail, \
    StudentLookHisSolution, StudentMessage
from course.views.person_view import UserRegister, ListPerson
from course.views.solution_view import SolutionToHomework

urlpatterns = [
    # Для удобства Login и Logout использовал Джанговский
    path('a-create-person/', UserRegister.as_view()),
    path('a-list-person/', ListPerson.as_view()),

    path('b-course-watch-and-add/all', CourseList.as_view()),
    path('b-course/detail/<int:pk>', DetailCourse.as_view()),
    path('b-course/add-professor/<int:course_id>', AddTeacher.as_view()),
    path('b-course/add_del-student/<int:course_id>', AddStudent.as_view()),

    path('bc-lecture-list/', LectureList.as_view()),
    path('c-lecture-add/<int:course_id>', LectureToCourse.as_view()),
    path('c-lecture-rud/<int:id>', LectureRUD.as_view()),

    path('d-add-homework/', HomeworkToLecture.as_view()),

    path('e-student-watch-task-and-add-solution/', SolutionToHomework.as_view()),

    path('eef-professor-watch-message/', ListMessageForProfessor.as_view()),
    path('ef-professor-watch-solutions-add-mark-message/', ProfessorWatchHomework.as_view()),
    path('f-professor-update-mark-message/<int:solution_id>', ProfessorMarkDetail.as_view()),

    path('g-student-look-check-solutions/', StudentLookHisSolution.as_view()),

    path('student-write-message/', StudentMessage.as_view())

]


from django.urls import path
from . import views

urlpatterns = [
    # instructor side urls
    path('instructor/', views.instructor_courses, name='instructor_courses'),
    path('instructor/add/', views.add_course, name='add_course'),
    path('instructor/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('instructor/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    # student side urls
    path('student/', views.student_course_list, name='student_course_list'),
    path('student/enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),

]

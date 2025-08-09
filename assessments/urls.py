from django.urls import path
from . import views

urlpatterns = [
    path('assessments/', views.assessment_list, name='assessment_list'),
    path('assessments/add/', views.add_assessment, name='add_assessment'),
    path('assessments/edit/<int:pk>/', views.edit_assessment, name='edit_assessment'),
    path('assessments/delete/<int:pk>/', views.delete_assessment, name='delete_assessment'),
    path('student/assessments/', views.student_assessments, name='student_assessments'),

]
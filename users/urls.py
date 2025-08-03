from django.urls import path
from .views import register_user, admin_dashboard, instructor_dashboard, student_dashboard, sponsor_dashboard, login_user, logout_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),



    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('instructor/dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('sponsor/dashboard/', sponsor_dashboard, name='sponsor_dashboard'),
    

]

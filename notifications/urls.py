from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.student_notifications,name='student_notifications'),
    path('mark-as-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
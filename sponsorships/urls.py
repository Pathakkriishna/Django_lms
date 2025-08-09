from django.urls import path
from . import views

urlpatterns = [
    path('fund/', views.fund_student, name='fund_student'),
    path('dashboard/', views.sponsor_dashboard, name='sponsor_dashboard'),
]


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assessment
from courses.models import Course
from django.contrib.auth.models import User
from notifications.models import Notification
from courses.models import Enrollment
from .forms import AssessmentForm 
from utils.email_utils import send_notification_email 

# View to list all assessments

def is_instructor(user):
    return user.groups.filter(name='Instructor').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

@user_passes_test(is_instructor)
@login_required
def assessment_list(request):
    assessments = Assessment.objects.all().order_by('-created_at')
    return render(request, 'assessments/assessment_list.html', {'assessments': assessments})

# View to create a new assessment
@user_passes_test(is_instructor)
@login_required
def add_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()

            # Get all students enrolled in the assessment's course
            enrolled_students = Enrollment.objects.filter(course=assessment.course)

            # Send notification to each enrolled student
            for enrollment in enrolled_students:
                Notification.objects.create(
                    user=enrollment.student,
                    message=f"New assessment '{assessment.title}' added in course: {assessment.course.title}"
                )
            # send email
            students = User.objects.filter(enrollments__course=assessment.course)
            recipient_list = [student.email for student in students if student.email]
            send_notification_email(
                subject="New Assessment Added",
                message=f"New assessment '{assessment.title}' added in course: {assessment.course.title}",
                recipient_list= recipient_list
            )

            return redirect('assessment_list')
    else:
        form = AssessmentForm()
    return render(request, 'assessments/add_assessment.html', {'form': form})

# View to edit an existing assessment
@user_passes_test(is_instructor)
@login_required
def edit_assessment(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    form = AssessmentForm(request.POST or None, instance=assessment)
    if form.is_valid():
        form.save()
        return redirect('assessment_list')
    return render(request, 'assessments/edit_assessment.html', {'form': form})

# View to delete an assessment
@user_passes_test(is_instructor)
@login_required
def delete_assessment(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    if request.method == 'POST':
        assessment.delete()
        return redirect('assessment_list')
    return render(request, 'assessments/delete_assessment.html', {'assessment': assessment})


@user_passes_test(is_student)
@login_required
def student_assessments(request):
    # Get enrolled courses for this student
    enrolled_courses = Course.objects.filter(enrollments__student=request.user)

    # Get assessments for those courses
    assessments = Assessment.objects.filter(course__in=enrolled_courses).order_by('due_date')

    return render(request, 'assessments/student_assessments.html', {'assessments': assessments})
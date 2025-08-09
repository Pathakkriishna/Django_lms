from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Enrollment
from notifications.models import Notification
from assessments.models import Assessment
from django.contrib.auth.models import User
from .forms import CourseForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator

# function to check wheather the logged in user is instructor or not
def is_instructor(user):
    return user.groups.filter(name='Instructor').exists()

# function to check wheather the logged in user is student or not
def is_student(user):
    return user.groups.filter(name='Student').exists()

# function to check wheather the logged in user is admin or not
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

# View to show list of courses created by the logged-in instructor
@login_required
@user_passes_test(is_instructor)
def instructor_courses(request):
    # Filter courses to only show those created by this instructor
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_courses.html', {'courses': courses})

# View to add a new course
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)  # Get the data user submitted
        if form.is_valid():
            course = form.save(commit=False)  # Don’t save yet, let’s attach instructor
            course.instructor = request.user
            course.save()  # Now save to database
            return redirect('instructor_courses')  # Go back to course list
    else:
        form = CourseForm()  # Show empty form for GET request
    return render(request, 'courses/add_course.html', {'form': form})

# View to update an existing course
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()  # Save the updated course
        return redirect('instructor_courses')
    return render(request, 'courses/edit_course.html', {'form': form})

# View to delete a course
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    course.delete()  # Delete this course
    return redirect('instructor_courses')


# This view displays all available courses and supports search
@login_required
@user_passes_test(is_student)
def student_course_list(request):
    query = request.GET.get('q')  # Get the text search query
    difficulty = request.GET.get('difficulty')  # Get difficulty filter
    courses = Course.objects.all()  # Start with all courses

    # If user typed something in search bar
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query) |
            Q(difficulty__icontains=query)
        )


    # If user selected difficulty from dropdown (Beginner, Intermediate, Advanced)
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    # Pagination
    paginator = Paginator(courses, 5)  # Show 5 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return the filtered courses to the template
    return render(request, 'courses/student_course_list.html', {
        'courses': page_obj,
        'selected_difficulty': difficulty or '',  # Pass current selected difficulty back to template
        'search_query': query or ''  # Pass current search term back to template
    })

# This view lets a logged-in student enroll in a course
@login_required
@user_passes_test(is_student)
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the student is already enrolled
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)

    # Send notification only if it's a new enrollment
    if created:
        Notification.objects.create(
            user=request.user,
            message=f"You have enrolled in the course: {course.title}"
        )

    return redirect('student_course_list')  


# Helper function to check if user is in Student group
def is_student(user):
    return user.groups.filter(name='Student').exists()

# Student Dashboard: Show courses the student is enrolled in
@user_passes_test(is_student)
@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'courses/student_dashboard.html', {'enrollments': enrollments})

#This view displays the courses in which the logged-in student is enrolled.
@login_required
@user_passes_test(is_student)
def enrolled_courses_view(request):
    # Get all enrollments for the currently logged-in user
    enrollments = Enrollment.objects.filter(student=request.user)

    # Extract the actual course objects from those enrollments
    courses = [enrollment.course for enrollment in enrollments]

    # Render the template with enrolled courses
    return render(request, 'courses/enrolled_courses.html', {'courses': courses})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_students': User.objects.filter(groups__name='Student').count(),
        'total_instructors': User.objects.filter(groups__name='Instructor').count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_assessments': Assessment.objects.count(),
        'total_notifications': Notification.objects.count(),
    }

    return render(request, 'admin/dashboard.html', context)
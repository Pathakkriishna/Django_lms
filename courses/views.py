from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Enrollment
from .forms import CourseForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q

# function to check wheather the logged in user is instructor or not
def is_instructor(user):
    return user.groups.filter(name='Instructor').exists()

# function to check wheather the logged in user is student or not
def is_student(user):
    return user.groups.filter(name='Student').exists()

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
    query = request.GET.get('q')  # Get search query from URL
    courses = Course.objects.all()  # Get all courses

    # If there is a search query, filter by title, description, instructor name, or difficulty
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query) |
            Q(difficulty__icontains=query)
        )

    return render(request, 'courses/student_course_list.html', {'courses': courses})

# This view lets a logged-in student enroll in a course
@login_required
@user_passes_test(is_student)
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get the course by ID
    Enrollment.objects.get_or_create(student=request.user, course=course)  # Enroll if not already enrolled
    return redirect('student_course_list')  # Redirect back to course list
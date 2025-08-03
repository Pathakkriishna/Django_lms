from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse


def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

def instructor_dashboard(request):
    return render(request, 'users/instructor_dashboard.html')
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')

def sponsor_dashboard(request):
    return render(request, 'users/sponsor_dashboard.html')



def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        group = Group.objects.get(name=role)
        user.groups.add(group)
        user.save()

        login(request, user)
        messages.success(
            request, f"Welcome {username}! You're registered as a {role}")
        return redirect('register')

    return render(request, 'users/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect to role-based dashboards
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Instructor').exists():
                return redirect('instructor_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            elif user.groups.filter(name='Sponsor').exists():
                return redirect('sponsor_dashboard')
            else:
                return redirect('home')  # fallback
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

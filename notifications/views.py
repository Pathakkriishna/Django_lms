from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Notification

def is_student(user):
    return user.groups.filter(name='Student').exists()

@login_required
@user_passes_test(is_student)
def student_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/student_notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk,user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('student_notifications')
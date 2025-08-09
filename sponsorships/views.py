from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SponsorshipForm
from .models import Sponsorship
from notifications.models import Notification

def is_sponsor(user):
    return user.groups.filter(name='Sponsor').exists()

@login_required
@user_passes_test(is_sponsor)
def fund_student(request):
    if request.method == 'POST':
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save(commit=False)
            sponsorship.sponsor = request.user
            sponsorship.save()

            # Create notification for student
            Notification.objects.create(
                user=sponsorship.student,
                message=f"You have been sponsored by {request.user.username} with ${sponsorship.amount}"
            )

            return redirect('sponsor_dashboard')  # or wherever sponsor dashboard is
    else:
        form = SponsorshipForm()

    return render(request, 'sponsors/fund_student.html', {'form': form})
@login_required
def sponsor_dashboard(request):
    sponsorships = Sponsorship.objects.filter(sponsor=request.user).select_related('student')
    return render(request, 'sponsors/sponsor_dashboard.html', {
        'sponsorships': sponsorships})

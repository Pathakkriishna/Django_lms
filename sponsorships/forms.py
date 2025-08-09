from django import forms
from .models import Sponsorship
from django.contrib.auth.models import User

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['student', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only students in dropdown
        self.fields['student'].queryset = User.objects.filter(groups__name='Student')

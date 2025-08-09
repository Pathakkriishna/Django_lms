
from django import forms
from .models import Assessment

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'course', 'description', 'due_date', 'total_marks']

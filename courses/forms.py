from django import forms
from .models import Course

# Form for creating and editing courses
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course  # Link this form to Course model
        fields = ['title', 'description', 'difficulty']  # These fields will show in the form

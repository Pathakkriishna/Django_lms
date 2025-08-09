from django import forms
from django.contrib.auth.models import User, Group

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[
        ('Admin', 'Admin'),
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
        ('Sponsor', 'Sponsor'),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

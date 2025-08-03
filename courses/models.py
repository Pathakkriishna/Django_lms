from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Choices for difficulty level in the course form
DIFFICULTY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

# Course model to represent a course in the LMS
class Course(models.Model):
    title = models.CharField(max_length=200)  # Title of the course
    description = models.TextField()          # Detailed course description
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)  # Who created this course
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)  # Difficulty level
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set to current date when created

    def __str__(self):
        return self.title  # When we print this model, it shows course title
    

# New model to store course enrollments
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # The enrolled student
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # The course they enrolled in
    date_enrolled = models.DateTimeField(auto_now_add=True)  # When they enrolled

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
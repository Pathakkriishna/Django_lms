from django.db import models
from courses.models import Course

# Create your models here.
class Assessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    total_marks = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')

    def __str__(self):
        return f"{self.title} ({self.course.title})"
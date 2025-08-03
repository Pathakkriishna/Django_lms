

from django.contrib import admin
from .models import Course, Enrollment  # import model

admin.site.register(Course)
admin.site.register(Enrollment)  # register model to admin site

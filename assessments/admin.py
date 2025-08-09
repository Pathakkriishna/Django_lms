from django.contrib import admin
from.models import Assessment
# Register your models here.

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'due_date', 'total_marks')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'created_at')
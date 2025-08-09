from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at', 'is_read')

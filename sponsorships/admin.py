from django.contrib import admin
from .models import Sponsorship

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'student', 'amount', 'sponsored_at')
    search_fields = ('sponsor__username', 'student__username')
    list_filter = ('sponsored_at',)

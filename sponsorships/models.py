from django.db import models
from django.contrib.auth.models import User

class Sponsorship(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsorships')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsored_by')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sponsored_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.username} sponsored {self.student.username}"

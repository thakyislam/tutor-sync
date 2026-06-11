from django.db import models
from django.conf import settings


class GuardianProfile(models.Model):
    PREFERRED_MODE = [
        ('online', 'Online'),
        ('in_person', 'In-Person'),
        ('both', 'Both'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardianprofile')
    address = models.TextField(blank=True)
    preferred_mode = models.CharField(max_length=20, choices=PREFERRED_MODE, default='both')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Guardian: {self.user.get_full_name() or self.user.username}'


class Student(models.Model):
    guardian = models.ForeignKey(GuardianProfile, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=200)
    grade = models.CharField(max_length=50)
    subjects_needed = models.ManyToManyField('core.Subject', blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} (Grade {self.grade})'

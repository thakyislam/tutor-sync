from django.db import models
from django.conf import settings


TUTOR_STATUS = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
]


class TutorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutorprofile')
    bio = models.TextField(blank=True)
    subjects = models.ManyToManyField('core.Subject', blank=True)
    education_level = models.CharField(max_length=100, blank=True)
    experience_yrs = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    availability = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=TUTOR_STATUS, default='inactive', db_index=True)
    verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Tutor: {self.user.get_full_name() or self.user.username}'


APPLICATION_STATUS = [
    ('submitted', 'Submitted'),
    ('under_review', 'Under Review'),
    ('interview', 'Interview'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class TutorApplication(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subjects = models.ManyToManyField('core.Subject', blank=True)
    education = models.TextField()
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    id_document = models.FileField(upload_to='ids/', blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='submitted', db_index=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_applications',
    )
    reviewer_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.full_name} ({self.get_status_display()})'

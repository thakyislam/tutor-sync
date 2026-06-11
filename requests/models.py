from django.db import models


class TutorRequest(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('matched', 'Matched'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    PREFERRED_MODE = [
        ('online', 'Online'),
        ('in_person', 'In-Person'),
        ('both', 'Both'),
    ]
    guardian = models.ForeignKey('guardians.GuardianProfile', on_delete=models.CASCADE, related_name='requests')
    student = models.ForeignKey('guardians.Student', on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey('core.Subject', on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=100)
    preferred_mode = models.CharField(max_length=20, choices=PREFERRED_MODE, default='both')
    budget = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    schedule_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending', db_index=True)
    assigned_tutor = models.ForeignKey(
        'tutors.TutorProfile',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_requests',
    )
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Request #{self.pk} — {self.get_status_display()}'

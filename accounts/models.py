from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('guardian', 'Guardian'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guardian', db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    def is_tutor(self):
        return self.role == 'tutor'

    def is_guardian(self):
        return self.role == 'guardian'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.role})'


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} to {self.recipient}'

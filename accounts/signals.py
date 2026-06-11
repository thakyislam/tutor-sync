from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.role == 'guardian':
        from guardians.models import GuardianProfile
        GuardianProfile.objects.get_or_create(user=instance)
    elif instance.role == 'tutor':
        from tutors.models import TutorProfile
        TutorProfile.objects.get_or_create(user=instance)

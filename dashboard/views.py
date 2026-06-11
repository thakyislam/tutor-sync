from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'admin' or user.is_staff:
        from accounts.models import User
        from tutors.models import TutorProfile, TutorApplication
        from requests.models import TutorRequest
        from guardians.models import GuardianProfile
        context = {
            'total_active_tutors': TutorProfile.objects.filter(status='active').count(),
            'total_guardians': GuardianProfile.objects.count(),
            'open_requests': TutorRequest.objects.filter(status='pending').count(),
            'pending_applications': TutorApplication.objects.filter(status='submitted').count(),
        }
        template = 'dashboard/admin.html'

    elif user.role == 'guardian':
        try:
            profile = user.guardianprofile
            from requests.models import TutorRequest
            context = {
                'active_requests': TutorRequest.objects.filter(
                    guardian=profile, status__in=['pending', 'matched']
                ).select_related('subject', 'assigned_tutor__user'),
                'students': profile.students.prefetch_related('subjects_needed'),
            }
        except Exception:
            context = {'active_requests': [], 'students': []}
        template = 'dashboard/guardian.html'

    elif user.role == 'tutor':
        try:
            profile = user.tutorprofile
            context = {'tutor': profile}
        except Exception:
            context = {}
        template = 'dashboard/tutor.html'

    else:
        template = 'dashboard/guardian.html'

    return render(request, template, context)

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'admin' or user.is_staff:
        from accounts.models import User
        from guardians.models import GuardianProfile
        from requests.models import TutorRequest
        from tutors.models import TutorApplication, TutorProfile

        recent_requests = list(
            TutorRequest.objects.select_related('guardian__user', 'subject').order_by('-updated_at')[:10]
        )
        for r in recent_requests:
            r.activity_type = 'request'

        recent_apps = list(TutorApplication.objects.order_by('-updated_at')[:10])
        for a in recent_apps:
            a.activity_type = 'application'

        recent_activity = sorted(
            chain(recent_requests, recent_apps),
            key=lambda x: x.updated_at,
            reverse=True,
        )[:10]

        context = {
            'total_active_tutors': TutorProfile.objects.filter(status='active').count(),
            'total_guardians': GuardianProfile.objects.count(),
            'open_requests': TutorRequest.objects.filter(status='pending').count(),
            'pending_applications': TutorApplication.objects.filter(status='submitted').count(),
            'recent_activity': recent_activity,
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

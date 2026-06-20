import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from core.models import Subject
from core.utils import notify

from .forms import ApplicationReviewForm, TutorApplicationForm, TutorProfileForm
from .models import APPLICATION_STATUS, TUTOR_STATUS, TutorApplication, TutorProfile


# ── Task 3.1 — Public Apply Form ─────────────────────────────────────

def tutor_apply(request):
    form = TutorApplicationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.status = 'submitted'
        application.save()
        form.save_m2m()
        detail_url = f'/admin/applications/{application.pk}/'
        for admin in User.objects.filter(role='admin'):
            notify(
                admin,
                title='New Tutor Application',
                message=f'{application.full_name} has submitted a tutor application.',
                link=detail_url,
            )
        return redirect('application_apply_success')
    return render(request, 'tutors/application_apply.html', {'form': form})


def application_apply_success(request):
    return render(request, 'tutors/application_apply_success.html')


# ── Task 3.2 — Application List (Admin) ──────────────────────────────

@role_required('admin')
def application_list(request):
    qs = TutorApplication.objects.select_related('reviewed_by')
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter in dict(APPLICATION_STATUS):
        qs = qs.filter(status=status_filter)

    pipeline = [
        (code, label, TutorApplication.objects.filter(status=code).count())
        for code, label in APPLICATION_STATUS
    ]

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'tutors/application_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': APPLICATION_STATUS,
        'pipeline': pipeline,
    })


# ── Task 3.3 — Application Detail + Review (Admin) ───────────────────

@role_required('admin')
def application_detail(request, pk):
    application = get_object_or_404(TutorApplication, pk=pk)
    form = ApplicationReviewForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        old_status = application.status
        updated = form.save(commit=False)
        updated.reviewed_by = request.user
        updated.save()
        if old_status != updated.status:
            try:
                applicant = User.objects.get(email=application.email)
                notify(
                    applicant,
                    title='Application Status Updated',
                    message=f'Your tutor application status is now "{updated.get_status_display()}".',
                )
            except User.DoesNotExist:
                pass
        messages.success(request, 'Application updated.')
        return redirect('application_detail', pk=pk)
    return render(request, 'tutors/application_detail.html', {
        'application': application,
        'form': form,
    })


# ── Task 3.4 — Approve → Create Tutor Account ────────────────────────

@role_required('admin')
def approve_to_tutor(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required.')
    application = get_object_or_404(TutorApplication, pk=pk)
    if application.status != 'approved':
        return HttpResponseBadRequest('Application must be in "approved" status before activating.')

    if User.objects.filter(email=application.email).exists():
        messages.error(request, f'A user account already exists for {application.email}.')
        return redirect('application_detail', pk=pk)

    parts = application.full_name.strip().split()
    first_name = parts[0]
    last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
    base_username = f'{first_name.lower()}.{last_name.lower()}'.strip('.')
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f'{base_username}{counter}'
        counter += 1

    raw_password = secrets.token_urlsafe(12)
    new_user = User.objects.create_user(
        username=username,
        email=application.email,
        password=raw_password,
        first_name=first_name,
        last_name=last_name,
        role='tutor',
    )
    new_user.tutorprofile.subjects.set(application.subjects.all())
    notify(
        new_user,
        title='Welcome to TutorSync!',
        message='Your tutor account has been activated. Sign in and complete your profile.',
        link='/login/',
    )

    return render(request, 'tutors/tutor_created.html', {
        'new_user': new_user,
        'raw_password': raw_password,
        'application': application,
    })


# ── Task 5.2 — Tutor List ────────────────────────────────────────────

@login_required
def tutor_list(request):
    is_admin = request.user.role == 'admin' or request.user.is_staff
    qs = TutorProfile.objects.select_related('user').prefetch_related('subjects')

    if not is_admin:
        qs = qs.filter(status='active')

    subject_filter = request.GET.get('subject', '')
    status_filter = request.GET.get('status', '')
    verified_filter = request.GET.get('verified', '')

    if subject_filter:
        qs = qs.filter(subjects__pk=subject_filter).distinct()
    if is_admin and status_filter:
        qs = qs.filter(status=status_filter)
    if is_admin and verified_filter in ('0', '1'):
        qs = qs.filter(verified=(verified_filter == '1'))

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'tutors/tutor_list.html', {
        'page_obj': page_obj,
        'subjects': Subject.objects.filter(is_active=True),
        'subject_filter': subject_filter,
        'status_filter': status_filter,
        'verified_filter': verified_filter,
        'status_choices': TUTOR_STATUS,
        'is_admin': is_admin,
    })


# ── Task 5.2 — Tutor Detail ──────────────────────────────────────────

@login_required
def tutor_detail(request, pk):
    tutor = get_object_or_404(
        TutorProfile.objects.select_related('user').prefetch_related('subjects'), pk=pk
    )
    is_admin = request.user.role == 'admin' or request.user.is_staff
    is_own = hasattr(request.user, 'tutorprofile') and request.user.tutorprofile.pk == pk
    return render(request, 'tutors/tutor_detail.html', {
        'tutor': tutor,
        'can_edit': is_admin or is_own,
        'is_admin': is_admin,
    })


# ── Task 5.3 — Tutor Profile Edit ────────────────────────────────────

@login_required
def tutor_edit(request, pk):
    tutor = get_object_or_404(TutorProfile, pk=pk)
    is_admin = request.user.role == 'admin' or request.user.is_staff
    is_own = hasattr(request.user, 'tutorprofile') and request.user.tutorprofile.pk == pk
    if not (is_admin or is_own):
        return HttpResponseForbidden('You do not have permission to edit this profile.')

    form = TutorProfileForm(request.POST or None, instance=tutor, is_admin=is_admin)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('tutor_detail', pk=pk)
    return render(request, 'tutors/tutor_edit.html', {
        'form': form,
        'tutor': tutor,
        'is_admin': is_admin,
    })

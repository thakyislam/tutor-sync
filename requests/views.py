import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from core.utils import notify

from .forms import RequestUpdateForm, TutorRequestForm
from .models import TutorRequest


def _filter_qs(request, qs):
    """Apply status/subject/date filters — used by both list and CSV export."""
    status_filter = request.GET.get('status', '')
    subject_filter = request.GET.get('subject', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if subject_filter:
        qs = qs.filter(subject__pk=subject_filter)
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    return qs


# ── Task 4.4 / 5.6 — Request List ───────────────────────────────────

@login_required
def request_list(request):
    from core.models import Subject
    user = request.user
    is_admin = user.role == 'admin' or user.is_staff

    base_qs = TutorRequest.objects.select_related(
        'guardian__user', 'subject', 'assigned_tutor__user', 'student'
    )

    if is_admin:
        qs = _filter_qs(request, base_qs)
    elif user.role == 'guardian':
        qs = base_qs.filter(guardian=user.guardianprofile)
    else:
        qs = base_qs.none()

    view_mode = request.GET.get('view', 'table') if is_admin else 'table'

    kanban_columns = []
    if is_admin and view_mode == 'kanban':
        all_reqs = list(qs.select_related('guardian__user', 'subject', 'student'))
        for code, label in TutorRequest.STATUS:
            kanban_columns.append({
                'code': code,
                'label': label,
                'requests': [r for r in all_reqs if r.status == code],
            })

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'requests/request_list.html', {
        'page_obj': page_obj,
        'status_filter': request.GET.get('status', ''),
        'subject_filter': request.GET.get('subject', ''),
        'date_from': request.GET.get('date_from', ''),
        'date_to': request.GET.get('date_to', ''),
        'status_choices': TutorRequest.STATUS,
        'subjects': Subject.objects.filter(is_active=True),
        'is_admin': is_admin,
        'view_mode': view_mode,
        'kanban_columns': kanban_columns,
    })


# ── Task 5.6 — CSV Export ────────────────────────────────────────────

@role_required('admin')
def request_export(request):
    qs = _filter_qs(
        request,
        TutorRequest.objects.select_related('guardian__user', 'subject', 'assigned_tutor__user', 'student'),
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="requests.csv"'
    writer = csv.writer(response)
    writer.writerow(['#', 'Guardian', 'Subject', 'Student', 'Level', 'Mode', 'Status', 'Assigned Tutor', 'Submitted'])
    for req in qs:
        writer.writerow([
            req.pk,
            req.guardian.user.get_full_name() or req.guardian.user.username,
            str(req.subject) if req.subject else '',
            req.student.name if req.student else '',
            req.level,
            req.get_preferred_mode_display(),
            req.get_status_display(),
            req.assigned_tutor.user.get_full_name() if req.assigned_tutor else '',
            req.created_at.strftime('%Y-%m-%d'),
        ])
    return response


# ── Task 4.3 — Submit Request (Guardian) ────────────────────────────

@role_required('guardian')
def request_create(request):
    guardian_profile = request.user.guardianprofile
    form = TutorRequestForm(request.POST or None, guardian_profile=guardian_profile)
    if request.method == 'POST' and form.is_valid():
        tutor_request = form.save(commit=False)
        tutor_request.guardian = guardian_profile
        tutor_request.status = 'pending'
        tutor_request.save()
        for admin in User.objects.filter(role='admin'):
            notify(
                admin,
                title='New Tutor Request',
                message=(
                    f'{request.user.get_full_name() or request.user.username} '
                    f'submitted a new tutor request.'
                ),
                link=f'/requests/{tutor_request.pk}/',
            )
        return redirect('request_detail', pk=tutor_request.pk)
    return render(request, 'requests/request_form.html', {'form': form})


# ── Task 4.5 — Request Detail ────────────────────────────────────────

@login_required
def request_detail(request, pk):
    user = request.user
    if user.role == 'guardian':
        tutor_request = get_object_or_404(TutorRequest, pk=pk, guardian=user.guardianprofile)
    else:
        tutor_request = get_object_or_404(TutorRequest, pk=pk)
    return render(request, 'requests/request_detail.html', {'request_obj': tutor_request})


# ── Task 4.6 — Assign Tutor & Update (Admin) ────────────────────────

@role_required('admin')
def request_update(request, pk):
    tutor_request = get_object_or_404(TutorRequest, pk=pk)
    form = RequestUpdateForm(request.POST or None, instance=tutor_request)
    if request.method == 'POST' and form.is_valid():
        updated = form.save()
        notify(
            tutor_request.guardian.user,
            title='Tutor Request Updated',
            message=f'Your request #{tutor_request.pk} status is now "{updated.get_status_display()}".',
            link=f'/requests/{tutor_request.pk}/',
        )
        if updated.assigned_tutor:
            notify(
                updated.assigned_tutor.user,
                title='You have been assigned a request',
                message=f'You have been assigned to tutor request #{tutor_request.pk}.',
                link=f'/requests/{tutor_request.pk}/',
            )
        messages.success(request, 'Request updated.')
        return redirect('request_detail', pk=pk)
    return render(request, 'requests/request_update.html', {
        'tutor_request': tutor_request,
        'form': form,
    })


# ── Task 4.7 — Cancel Request (Guardian) ────────────────────────────

@login_required
def request_cancel(request, pk):
    if request.user.role != 'guardian':
        return HttpResponseBadRequest('Only guardians can cancel requests.')
    tutor_request = get_object_or_404(TutorRequest, pk=pk, guardian=request.user.guardianprofile)
    if tutor_request.status != 'pending':
        messages.error(request, 'Only pending requests can be cancelled.')
        return redirect('request_detail', pk=pk)
    if request.method == 'POST':
        tutor_request.status = 'cancelled'
        tutor_request.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Request cancelled.')
        return redirect('request_list')
    return render(request, 'requests/request_cancel_confirm.html', {'request_obj': tutor_request})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required

from .forms import GuardianCreateForm, StudentForm
from .models import GuardianProfile, Student


# ── Task 5.4 — Guardian List (Admin) ─────────────────────────────────

@role_required('admin')
def guardian_list(request):
    q = request.GET.get('q', '')
    qs = GuardianProfile.objects.select_related('user').annotate(student_count=Count('students'))
    if q:
        qs = qs.filter(
            Q(user__email__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__username__icontains=q)
        )
    paginator = Paginator(qs.order_by('-created_at'), 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'guardians/guardian_list.html', {'page_obj': page_obj, 'q': q})


# ── Task 5.4 — Guardian Detail (Admin) ───────────────────────────────

@role_required('admin')
def guardian_detail(request, pk):
    profile = get_object_or_404(GuardianProfile.objects.select_related('user'), pk=pk)
    students = profile.students.prefetch_related('subjects_needed')
    tutor_requests = profile.requests.select_related('subject', 'assigned_tutor__user').order_by('-created_at')
    return render(request, 'guardians/guardian_detail.html', {
        'profile': profile,
        'students': students,
        'tutor_requests': tutor_requests,
    })


# ── Task 5.4 — Deactivate Guardian (Admin) ───────────────────────────

@role_required('admin')
def guardian_deactivate(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required.')
    profile = get_object_or_404(GuardianProfile, pk=pk)
    profile.user.is_active = False
    profile.user.save(update_fields=['is_active'])
    messages.success(request, f'{profile.user.get_full_name() or profile.user.username} has been deactivated.')
    return redirect('guardian_list')


# ── Task 5.5 — Create Guardian (Admin) ───────────────────────────────

@role_required('admin')
def guardian_add(request):
    form = GuardianCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'Guardian account created for {user.get_full_name() or user.username}.')
        return redirect('guardian_detail', pk=user.guardianprofile.pk)
    return render(request, 'guardians/guardian_add.html', {'form': form})


# ── Task 4.2 — Student Management (Guardian) ─────────────────────────

@role_required('guardian')
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.guardian = request.user.guardianprofile
        student.save()
        form.save_m2m()
        return redirect('dashboard')
    return render(request, 'guardians/student_form.html', {'form': form, 'student': None})


@role_required('guardian')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk, guardian=request.user.guardianprofile)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'guardians/student_form.html', {'form': form, 'student': student})

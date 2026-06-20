from axes.exceptions import AxesBackendRequestParameterRequired
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import (
    AdminUserCreateForm, AdminUserEditForm,
    GuardianRegistrationForm, LoginForm, ProfileForm, StyledPasswordChangeForm,
)
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'dashboard'))
    if request.method == 'POST' and not form.is_valid():
        for error in form.non_field_errors():
            if 'locked' in str(error).lower() or 'attempt' in str(error).lower():
                messages.error(request, 'Too many failed login attempts. Please try again later.')
                break
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = GuardianRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome to TutorSync.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def notification_list_view(request):
    notifications = request.user.notifications.all()
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notification_list.html', {'notifications': notifications})


@login_required
def password_change_view(request):
    form = StyledPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('profile')
    return render(request, 'accounts/password_change.html', {'form': form})


# ── Task 5.7 — Admin User Management ────────────────────────────────

@role_required('admin')
def admin_user_list(request):
    q = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    qs = User.objects.all()
    if q:
        from django.db.models import Q
        qs = qs.filter(
            Q(username__icontains=q) | Q(email__icontains=q) |
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    if role_filter:
        qs = qs.filter(role=role_filter)
    paginator = Paginator(qs.order_by('role', 'username'), 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'accounts/admin_user_list.html', {
        'page_obj': page_obj,
        'q': q,
        'role_filter': role_filter,
        'role_choices': User.ROLE_CHOICES,
    })


@role_required('admin')
def admin_user_create(request):
    form = AdminUserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'Account created for {user.get_full_name() or user.username}.')
        return redirect('admin_user_list')
    return render(request, 'accounts/admin_user_form.html', {'form': form, 'target_user': None})


@role_required('admin')
def admin_user_edit(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    form = AdminUserEditForm(request.POST or None, instance=target_user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated.')
        return redirect('admin_user_list')
    return render(request, 'accounts/admin_user_form.html', {'form': form, 'target_user': target_user})

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TutorSync is a Django-based Tutor Management System that replaces spreadsheet workflows for managing tutors, guardians (parents), and tutor requests. Three roles: `admin`, `tutor`, `guardian`.

## Commands

```bash
python manage.py runserver          # Dev server at http://127.0.0.1:8000
python manage.py check              # Validate project configuration
python manage.py check --deploy     # Production readiness check
python manage.py makemigrations     # Generate migrations after model changes
python manage.py migrate            # Apply migrations (SQLite)
python manage.py collectstatic      # Collect static files (WhiteNoise serves them)
python manage.py createsuperuser    # Create admin user (set role='admin')
gunicorn config.wsgi:application -c gunicorn.conf.py  # Production server
```

There is no test suite, linter, or formatter configured.

## Architecture

### Config & Settings

- Project config lives in `config/` (not a flat `settings.py`). Entry point: `config.settings`.
- Secrets loaded via `python-decouple` from `.env` (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`).
- `AUTH_USER_MODEL = 'accounts.User'` — custom AbstractUser with a `role` field.
- `STORAGES` uses WhiteNoise's `CompressedManifestStaticFilesStorage`.

### App Responsibilities

| App | What it owns |
|---|---|
| `accounts` | User model, Notification model, login/logout/register, profile, password change, admin user management, `@role_required` decorator, `post_save` signal for auto-creating profiles, notification context processor |
| `tutors` | TutorProfile, TutorApplication, public `/apply/` form, admin application review pipeline, tutor directory/detail/edit |
| `guardians` | GuardianProfile, Student, admin guardian management, guardian self-service student CRUD |
| `requests` | TutorRequest, request creation/list/detail/update/cancel, kanban/table toggle, CSV export |
| `dashboard` | Role-dispatched dashboard view (admin gets stats + KPIs, guardian gets their requests + students) |
| `core` | Subject model (shared M2M target), `notify()` helper |

### The `requests` App Name Conflict

The `requests` app collides with Python's `requests` stdlib. It uses `label = 'tutor_requests'` in its `AppConfig` and is registered as `'requests.apps.RequestsConfig'` in INSTALLED_APPS.

### Role System & Access Control

- `accounts.decorators.role_required(*roles)` — wraps `@login_required`, returns 403 if `user.role` not in allowed roles. Superusers bypass the check.
- Admin-only URLs are under `/admin/` prefix (separate from Django admin at `/admin/`). Guardian URLs under `/guardians/`, `/requests/`.
- Ownership checks are manual in views (e.g., `Student` must belong to `request.user.guardianprofile`).

### Auto-Profile Signal

`accounts.signals.create_role_profile` — on `User` post_save (created only):
- `role='guardian'` → creates `GuardianProfile`
- `role='tutor'` → creates `TutorProfile`

This means creating a User with a role always produces the matching profile. Views can safely access `user.guardianprofile` or `user.tutorprofile` for users with the correct role.

### Notification System

- `core.utils.notify(recipient, title, message, link='')` creates a `Notification` record.
- `accounts.context_processors.notifications` injects `unread_count` and `recent_notifications` into every template context.
- Notifications are in-app only (no email).

### URL Name Conventions

Key URL names used in `redirect()` and `{% url %}` calls:
- `dashboard`, `login`, `logout`, `register`, `profile`
- `tutor_list`, `tutor_detail`, `tutor_edit`, `tutor_apply`
- `application_list`, `application_detail`, `approve_to_tutor`
- `guardian_list`, `guardian_detail_admin`, `guardian_add`, `guardian_deactivate`
- `student_add`, `student_edit`
- `request_list`, `request_create`, `request_detail`, `request_update`, `request_cancel`, `request_export`
- `admin_user_list`, `admin_user_create`, `admin_user_edit`
- `notifications`, `password_change`

### Templates

- `templates/base.html` — main layout with sidebar + topbar. App pages extend this.
- `templates/base_auth.html` — split-panel layout for login/register.
- `templates/components/` — reusable includes: `logo.html`, `sidebar.html`, `topbar.html`, `badge.html`, `empty_state.html`, `pagination.html`.
- CSS classes are prefixed `ts-` (e.g., `ts-btn`, `ts-card`, `ts-badge-pending`).
- Tailwind CSS loaded via CDN. Lucide Icons initialized in `static/js/app.js`.

### Static & Media

- `static/` — source static files (CSS, JS, images). `staticfiles/` — collectstatic output.
- `media/` — user uploads. Subdirs: `avatars/`, `resumes/`, `ids/`.
- File upload validation: resumes accept PDF/DOC/DOCX (≤10MB), avatars accept JPG/PNG/GIF/WebP (≤5MB).

### Security

- `django-axes` for login rate limiting (5 failures, 1hr cooloff, locked by username+IP).
- All POST forms use `{% csrf_token %}`. No `| safe` or `mark_safe` on user data.
- Production mode (`DEBUG=False`) enables HSTS, secure cookies, SSL redirect.

### Database

SQLite at `db.sqlite3`. No migration squashing has been done. Indexed fields: `User.role`, `TutorRequest.status`, `TutorRequest.created_at`, `TutorApplication.status`, `TutorProfile.status`.

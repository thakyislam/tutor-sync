# Tutor Management System — Technical Specification

**Project:** Centralized Tutor Management Web Application & Admin Panel  
**Tech Stack:** Django · SQLite · Tailwind CSS · Lucide Icons  
**Version:** 1.0  
**Date:** June 2026  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Objectives](#2-goals--objectives)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack Details](#4-tech-stack-details)
5. [Database Design (ERD)](#5-database-design-erd)
6. [Module Breakdown](#6-module-breakdown)
7. [URL Structure & Routing](#7-url-structure--routing)
8. [User Roles & Permissions](#8-user-roles--permissions)
9. [Key Workflows](#9-key-workflows)
10. [UI/UX Conventions](#10-uiux-conventions)
11. [Admin Panel Features](#11-admin-panel-features)
12. [Security Considerations](#12-security-considerations)
13. [Performance Considerations](#13-performance-considerations)
14. [Folder Structure](#14-folder-structure)
15. [Milestones & Delivery Plan](#15-milestones--delivery-plan)

---

## 1. Project Overview

The Tutor Management System (TMS) is a centralized web platform built with Django that replaces all dependency on external spreadsheets (Google Sheets, Excel, etc.) for managing tutor requests, tutor applications, guardian profiles, tutor profiles, and platform administrators. It provides a single source of truth for all operational data, with a custom admin panel offering granular control over each entity.

---

## 2. Goals & Objectives

| # | Goal | Outcome |
|---|------|---------|
| G1 | Remove external sheet dependency | All data lives in SQLite via Django ORM |
| G2 | Streamline operational workflow | Status-driven pipelines with in-app notifications |
| G3 | Centralized management | One dashboard for admins covering all entities |
| G4 | Guardian self-service | Guardians submit and track tutor requests online |
| G5 | Tutor application pipeline | End-to-end tutor onboarding within the system |
| G6 | Performance optimization | Querysets, pagination, and caching for large datasets |
| G7 | Role-based access control | Admins, tutors, and guardians see only what they need |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Client Browser                   │
│              Tailwind CSS  +  Lucide Icons              │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/HTTPS
┌────────────────────────▼────────────────────────────────┐
│                    Django Application                    │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  accounts/   │  │   tutors/    │  │  guardians/  │  │
│  │  (auth +     │  │  (profiles,  │  │  (profiles,  │  │
│  │   roles)     │  │  applications│  │   requests)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  requests/   │  │  dashboard/  │  │   admin_     │  │
│  │  (tutor      │  │  (stats,     │  │   panel/     │  │
│  │   matching)  │  │   overview)  │  │  (custom UI) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │             Django ORM / SQLite DB               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

The system follows Django's MVT (Model–View–Template) pattern. Each domain area is an independent Django app with its own models, views, URLs, and templates.

---

## 4. Tech Stack Details

### 4.1 Backend — Django

| Component | Detail |
|-----------|--------|
| Framework | Django 5.x |
| Language | Python 3.12+ |
| ORM | Django ORM (SQLite) |
| Auth | `django.contrib.auth` + custom `AbstractUser` |
| Forms | Django ModelForms + crispy-forms |
| Admin | Custom Django admin with extended ModelAdmin classes |
| Sessions | Django sessions (cookie-based) |
| Environment | `python-decouple` for `.env` management |

### 4.2 Database — SQLite

SQLite is used for its zero-configuration setup. All migrations are managed via Django's migration framework. For production scaling, the ORM abstraction allows migration to PostgreSQL with minimal configuration changes.

### 4.3 Frontend — Tailwind CSS

- Tailwind CSS v3 via CDN or PostCSS build pipeline
- Custom `tailwind.config.js` with extended color palette and font settings
- Component patterns: Cards, Badges, Modals, Drawers, Tables, Forms
- Responsive design with mobile-first breakpoints (`sm`, `md`, `lg`, `xl`)

### 4.4 Icons — Lucide Icons

- Lucide Icons via CDN (`lucide` JS library)
- Icons rendered inline via `<i data-lucide="icon-name">` or as SVG sprites
- Used for navigation, action buttons, status badges, and empty-state illustrations

---

## 5. Database Design (ERD)

### 5.1 Core Models

#### `User` (accounts app — extends AbstractUser)

```python
class User(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'), ('tutor', 'Tutor'), ('guardian', 'Guardian')]
    role        = CharField(max_length=20, choices=ROLE_CHOICES)
    phone       = CharField(max_length=20, blank=True)
    avatar      = ImageField(upload_to='avatars/', blank=True)
    created_at  = DateTimeField(auto_now_add=True)
    is_active   = BooleanField(default=True)
```

---

#### `TutorProfile` (tutors app)

```python
class TutorProfile(Model):
    user            = OneToOneField(User, on_delete=CASCADE)
    bio             = TextField(blank=True)
    subjects        = ManyToManyField('Subject')
    education_level = CharField(max_length=100)
    experience_yrs  = PositiveIntegerField(default=0)
    hourly_rate     = DecimalField(max_digits=8, decimal_places=2)
    availability    = JSONField(default=dict)        # e.g. {"Mon": ["09:00","17:00"]}
    status          = CharField(choices=TUTOR_STATUS) # active, inactive, suspended
    verified        = BooleanField(default=False)
    rating          = DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at      = DateTimeField(auto_now_add=True)
    updated_at      = DateTimeField(auto_now=True)
```

---

#### `GuardianProfile` (guardians app)

```python
class GuardianProfile(Model):
    user            = OneToOneField(User, on_delete=CASCADE)
    address         = TextField(blank=True)
    preferred_mode  = CharField(choices=[('online','Online'),('in_person','In-Person'),('both','Both')])
    notes           = TextField(blank=True)
    created_at      = DateTimeField(auto_now_add=True)
```

---

#### `Student` (guardians app)

```python
class Student(Model):
    guardian        = ForeignKey(GuardianProfile, on_delete=CASCADE, related_name='students')
    name            = CharField(max_length=200)
    grade           = CharField(max_length=50)
    subjects_needed = ManyToManyField('Subject')
    notes           = TextField(blank=True)
```

---

#### `TutorRequest` (requests app)

```python
class TutorRequest(Model):
    STATUS = [('pending','Pending'),('matched','Matched'),('closed','Closed'),('cancelled','Cancelled')]
    guardian        = ForeignKey(GuardianProfile, on_delete=CASCADE)
    student         = ForeignKey(Student, on_delete=SET_NULL, null=True)
    subject         = ForeignKey('Subject', on_delete=SET_NULL, null=True)
    level           = CharField(max_length=100)
    preferred_mode  = CharField(max_length=20)
    budget          = DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    schedule_notes  = TextField(blank=True)
    status          = CharField(max_length=20, choices=STATUS, default='pending')
    assigned_tutor  = ForeignKey(TutorProfile, null=True, blank=True, on_delete=SET_NULL)
    admin_notes     = TextField(blank=True)
    created_at      = DateTimeField(auto_now_add=True)
    updated_at      = DateTimeField(auto_now=True)
```

---

#### `TutorApplication` (tutors app)

```python
class TutorApplication(Model):
    STATUS = [('submitted','Submitted'),('under_review','Under Review'),
              ('interview','Interview'),('approved','Approved'),('rejected','Rejected')]
    applicant       = ForeignKey(User, on_delete=CASCADE)
    full_name       = CharField(max_length=200)
    email           = EmailField()
    phone           = CharField(max_length=20)
    subjects        = ManyToManyField('Subject')
    education       = TextField()
    experience      = TextField()
    resume          = FileField(upload_to='resumes/')
    id_document     = FileField(upload_to='ids/', blank=True)
    status          = CharField(max_length=20, choices=STATUS, default='submitted')
    reviewed_by     = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL,
                                 related_name='reviewed_applications')
    reviewer_notes  = TextField(blank=True)
    submitted_at    = DateTimeField(auto_now_add=True)
    updated_at      = DateTimeField(auto_now=True)
```

---

#### `Subject` (core/shared)

```python
class Subject(Model):
    name        = CharField(max_length=100, unique=True)
    category    = CharField(max_length=100, blank=True)
    is_active   = BooleanField(default=True)
```

---

#### `Notification` (accounts app)

```python
class Notification(Model):
    recipient   = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
    title       = CharField(max_length=200)
    message     = TextField()
    link        = CharField(max_length=500, blank=True)
    is_read     = BooleanField(default=False)
    created_at  = DateTimeField(auto_now_add=True)
```

---

### 5.2 Relationships Summary

```
User ──────────── TutorProfile (1:1)
User ──────────── GuardianProfile (1:1)
GuardianProfile ── Student (1:N)
GuardianProfile ── TutorRequest (1:N)
TutorRequest ───── TutorProfile (N:1, nullable)
TutorRequest ───── Subject (N:1)
TutorRequest ───── Student (N:1)
TutorProfile ────── Subject (M:M)
TutorApplication ── Subject (M:M)
User ──────────── Notification (1:N)
```

---

## 6. Module Breakdown

### 6.1 `accounts` App

**Responsibilities:** User registration, login/logout, role assignment, password management, notifications.

| View | URL | Description |
|------|-----|-------------|
| `LoginView` | `/login/` | Role-aware login with redirect |
| `RegisterView` | `/register/` | Guardian self-registration |
| `LogoutView` | `/logout/` | Session clear |
| `ProfileView` | `/profile/` | View/edit own profile |
| `NotificationListView` | `/notifications/` | All notifications, mark-as-read |
| `ChangePasswordView` | `/password/change/` | Password update |

---

### 6.2 `tutors` App

**Responsibilities:** Tutor profiles, tutor applications, subject management.

| View | URL | Description |
|------|-----|-------------|
| `TutorListView` | `/tutors/` | Paginated, filterable tutor directory |
| `TutorDetailView` | `/tutors/<id>/` | Tutor profile page |
| `TutorApplicationCreateView` | `/apply/` | Public application form |
| `TutorApplicationListView` | `/admin/applications/` | Admin: all applications |
| `TutorApplicationDetailView` | `/admin/applications/<id>/` | Admin: review & update status |
| `TutorEditView` | `/tutors/<id>/edit/` | Admin: edit tutor profile |

---

### 6.3 `guardians` App

**Responsibilities:** Guardian profiles, student management.

| View | URL | Description |
|------|-----|-------------|
| `GuardianListView` | `/admin/guardians/` | Admin: all guardians |
| `GuardianDetailView` | `/admin/guardians/<id>/` | Admin: guardian profile & students |
| `StudentCreateView` | `/guardians/students/add/` | Guardian: add student |
| `StudentEditView` | `/guardians/students/<id>/edit/` | Guardian: edit student |

---

### 6.4 `requests` App

**Responsibilities:** Tutor request submission, tracking, matching, and closure.

| View | URL | Description |
|------|-----|-------------|
| `RequestCreateView` | `/requests/new/` | Guardian: submit tutor request |
| `RequestListView` | `/requests/` | Guardian: own requests; Admin: all |
| `RequestDetailView` | `/requests/<id>/` | View request detail |
| `RequestUpdateView` | `/requests/<id>/edit/` | Admin: assign tutor, update status |
| `RequestCancelView` | `/requests/<id>/cancel/` | Guardian: cancel pending request |

---

### 6.5 `dashboard` App

**Responsibilities:** Role-based dashboards with KPIs and quick-action shortcuts.

| Role | Dashboard Features |
|------|--------------------|
| Admin | Total requests, pending applications, active tutors, recent activity feed, quick-link cards |
| Tutor | Assigned sessions, profile completeness, notification inbox |
| Guardian | Active requests, linked students, request history |

---

## 7. URL Structure & Routing

```
/                           → Redirect to dashboard (if logged in) or login
/login/                     → Login
/logout/                    → Logout
/register/                  → Guardian self-registration
/dashboard/                 → Role-based dashboard
/profile/                   → Own profile view/edit
/notifications/             → Notification list

/apply/                     → Public tutor application form
/tutors/                    → Tutor directory (admin/guardian)
/tutors/<id>/               → Tutor detail
/tutors/<id>/edit/          → Admin: edit tutor

/requests/                  → Request list (role-filtered)
/requests/new/              → Submit request
/requests/<id>/             → Request detail
/requests/<id>/edit/        → Admin: update/assign
/requests/<id>/cancel/      → Cancel request

/admin/applications/        → Application list
/admin/applications/<id>/   → Application detail & review
/admin/guardians/           → Guardian list
/admin/guardians/<id>/      → Guardian detail

/admin/                     → Django built-in admin (superuser only)
```

---

## 8. User Roles & Permissions

### Role Matrix

| Feature | Guardian | Tutor | Admin |
|---------|----------|-------|-------|
| Submit tutor request | ✅ | ❌ | ✅ |
| View own requests | ✅ | ❌ | ✅ |
| View all requests | ❌ | ❌ | ✅ |
| Assign tutor to request | ❌ | ❌ | ✅ |
| Apply as tutor | ✅ (public) | — | — |
| View all applications | ❌ | ❌ | ✅ |
| Update application status | ❌ | ❌ | ✅ |
| View tutor directory | ✅ | ✅ | ✅ |
| Edit tutor profiles | ❌ | Own only | ✅ |
| View all guardians | ❌ | ❌ | ✅ |
| Manage subjects | ❌ | ❌ | ✅ |
| Manage admin users | ❌ | ❌ | ✅ |
| View dashboard stats | Own | Own | All |

### Permission Implementation

Permissions are enforced via:
1. Django's `@login_required` decorator for all authenticated views
2. Custom `role_required(role)` decorator for role-gated views
3. `UserPassesTestMixin` in class-based views for object-level access
4. Template-level `{% if user.role == 'admin' %}` checks for UI elements

---

## 9. Key Workflows

### 9.1 Guardian Submits a Tutor Request

```
Guardian logs in
    → Dashboard → "New Request" button
    → Fills RequestCreateForm (student, subject, level, mode, budget, schedule)
    → Request saved with status: PENDING
    → Notification sent to all admins
    → Guardian sees request in "My Requests" list with PENDING badge
```

### 9.2 Admin Reviews & Matches a Request

```
Admin receives notification
    → Admin Dashboard → Pending Requests
    → Opens RequestDetailView
    → Reviews details → clicks "Assign Tutor"
    → Selects from available tutors filtered by subject
    → Status updated to MATCHED
    → Notifications sent to Guardian and assigned Tutor
    → Admin can add internal notes
```

### 9.3 Tutor Application Pipeline

```
Applicant visits /apply/ (no login required)
    → Fills TutorApplicationForm (personal info, subjects, resume upload)
    → Application saved with status: SUBMITTED
    → Admin notified
    → Admin opens application → reviews → changes status:
        SUBMITTED → UNDER_REVIEW → INTERVIEW → APPROVED / REJECTED
    → On APPROVED: Admin creates User account + TutorProfile for applicant
    → Applicant emailed with login credentials
```

### 9.4 Admin Creates a Guardian Account

```
Admin → /admin/guardians/ → "Add Guardian"
    → Fills user creation form (name, email, phone, password)
    → GuardianProfile auto-created via post_save signal
    → Guardian can log in and add students from their profile
```

---

## 10. UI/UX Conventions

### Layout

- **Sidebar navigation** (collapsible on mobile) with Lucide icons per section
- **Topbar** with user avatar, role badge, notification bell (with unread count), logout
- **Main content area** with breadcrumb navigation
- **Responsive tables** with horizontal scroll on small screens
- **Empty state illustrations** using Lucide icon + message for zero-data views

### Status Badges (Tailwind)

| Status | Badge Class |
|--------|-------------|
| Pending | `bg-yellow-100 text-yellow-800` |
| Under Review | `bg-blue-100 text-blue-800` |
| Matched / Approved | `bg-green-100 text-green-800` |
| Rejected / Cancelled | `bg-red-100 text-red-800` |
| Closed | `bg-gray-100 text-gray-600` |
| Interview | `bg-purple-100 text-purple-800` |

### Key Lucide Icons Used

| Context | Icon |
|---------|------|
| Dashboard | `layout-dashboard` |
| Tutors | `graduation-cap` |
| Guardians | `users` |
| Requests | `file-text` |
| Applications | `clipboard-list` |
| Notifications | `bell` |
| Settings | `settings` |
| Add/Create | `plus-circle` |
| Edit | `pencil` |
| Delete | `trash-2` |
| Status/Check | `check-circle` |
| Reject | `x-circle` |
| Logout | `log-out` |

### Forms

- All forms use ModelForm with field validation
- Error messages displayed inline below each field
- `crispy-forms` with Tailwind template pack for consistent styling
- File upload fields show current file name and allow replacement

---

## 11. Admin Panel Features

The custom admin panel (built as a Django app, separate from `django.contrib.admin`) provides:

### Dashboard Overview Cards
- Total active tutors, total guardians, open requests, pending applications
- Recent activity feed (latest 10 actions across all entities)
- Quick-action shortcuts: "Review Applications", "Unassigned Requests"

### Tutor Management
- Paginated list with filters: subject, status, verified, date joined
- Bulk actions: activate, deactivate, verify
- Detail view with full profile, application history, and assigned requests
- Inline status and note editing

### Guardian Management
- Paginated list with search by name/email
- Detail view showing linked students and all submitted requests
- Ability to add notes or deactivate accounts

### Request Management
- Kanban-style status board OR sortable table view (toggle)
- Filter by status, subject, guardian, assigned tutor, date range
- Assign/reassign tutor inline from the list
- Export filtered view to CSV

### Application Management
- Pipeline view showing count per stage
- Review form with status dropdown, reviewer notes, and document preview
- One-click conversion: APPROVED application → create Tutor account

### User/Admin Management
- Create new admin users
- Deactivate accounts (soft delete)
- Role reassignment
- Activity log per user

---

## 12. Security Considerations

| Area | Measure |
|------|---------|
| Authentication | Session-based auth; passwords hashed via Django's `PBKDF2` |
| CSRF | Django CSRF middleware enabled on all POST forms |
| Authorization | `login_required` + role checks on every protected view |
| File Uploads | Validate MIME type and extension; store outside `MEDIA_ROOT` web path |
| SQL Injection | Django ORM parameterized queries; no raw SQL unless absolutely needed |
| XSS | Django auto-escaping in templates; avoid `mark_safe` unless sanitized |
| Secret Key | Stored in `.env`, loaded via `python-decouple`; never committed |
| DEBUG Mode | `DEBUG=False` in production; custom 404/500 error pages |
| Admin Access | `/admin/` restricted to `is_superuser=True` only |
| Rate Limiting | Implement `django-axes` for login attempt throttling |

---

## 13. Performance Considerations

| Concern | Solution |
|---------|----------|
| Large tutor/request lists | `Paginator` (20 items/page default) |
| N+1 query problem | `select_related()` and `prefetch_related()` on ForeignKey/M2M fields |
| Repeated queryset calls | `QuerySet.cache()` or template fragment caching |
| Static assets | `django-compressor` or WhiteNoise for CSS/JS serving |
| Database indexes | Add `db_index=True` on frequently filtered fields (status, role, created_at) |
| File storage | Use `django-storages` with local filesystem; swap to S3 for scale-up |
| Search queries | `Q` objects with `__icontains` on indexed fields; add `django-filter` for complex filtering |

---

## 14. Folder Structure

```
tutor_management/
│
├── manage.py
├── requirements.txt
├── .env
├── tailwind.config.js
│
├── config/                     # Project settings package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                   # Users, auth, notifications
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── decorators.py           # role_required decorator
│   ├── signals.py
│   └── templates/accounts/
│
├── tutors/                     # Tutor profiles & applications
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/tutors/
│
├── guardians/                  # Guardian profiles & students
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/guardians/
│
├── requests/                   # Tutor requests
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/requests/
│
├── dashboard/                  # Role-based dashboards
│   ├── views.py
│   ├── urls.py
│   └── templates/dashboard/
│
├── core/                       # Shared models (Subject), utilities
│   ├── models.py
│   ├── utils.py
│   └── templatetags/
│
├── static/
│   ├── css/
│   │   └── main.css            # Compiled Tailwind output
│   ├── js/
│   │   └── app.js              # Lucide init + UI helpers
│   └── img/
│
├── media/                      # User-uploaded files (resumes, avatars)
│
└── templates/
    ├── base.html               # Master layout: sidebar, topbar, footer
    ├── components/
    │   ├── sidebar.html
    │   ├── topbar.html
    │   ├── badge.html
    │   ├── empty_state.html
    │   └── pagination.html
    └── errors/
        ├── 404.html
        └── 500.html
```

---

## 15. Milestones & Delivery Plan

| Phase | Milestone | Key Deliverables |
|-------|-----------|-----------------|
| **Phase 1** | Foundation | Project scaffolding, Django apps, base templates, auth (login/register/logout), User model with roles |
| **Phase 2** | Core Data Models | TutorProfile, GuardianProfile, Student, Subject migrations + Django admin registration |
| **Phase 3** | Tutor Application Flow | Public `/apply/` form, application list & review views for admin, status pipeline |
| **Phase 4** | Guardian & Request Flow | Guardian dashboard, student management, TutorRequest create/list/detail/assign |
| **Phase 5** | Admin Panel UI | Custom admin dashboard, all management views, bulk actions, CSV export |
| **Phase 6** | Notifications & Polish | In-app notifications, responsive UI polish, empty states, loading states |
| **Phase 7** | QA & Security Review | Role permission audit, query optimization, CSRF/XSS checks, test coverage |
| **Phase 8** | Deployment | WhiteNoise static files, `gunicorn` + `nginx` config, `.env` hardening |

---

## Appendix A — Key Python Dependencies

```txt
Django>=5.0
Pillow                    # ImageField support
django-crispy-forms
crispy-tailwind
django-filter
django-axes               # Login rate limiting
python-decouple           # .env management
whitenoise                # Static file serving
gunicorn                  # WSGI server (production)
```

---

## Appendix B — Tailwind Config Highlights

```js
// tailwind.config.js
module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#2563EB', light: '#DBEAFE', dark: '#1E40AF' },
        accent:  { DEFAULT: '#7C3AED', light: '#EDE9FE' },
      },
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
        display: ['Cal Sans', 'sans-serif'],
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
```

---

*End of Technical Specification — Tutor Management System v1.0*
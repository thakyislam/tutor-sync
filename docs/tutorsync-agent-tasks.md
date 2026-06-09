# TutorSync — Claude Agent Task List

**Project:** Tutor Management System (TMS)  
**Reference Spec:** `docs/tutorsync-technical-specification.md`  
**Format:** Each task is self-contained and actionable for a coding agent.  
**Date:** June 2026

---

## How to Use This Document

Work through phases in order. Each task block contains:
- **Goal** — what must exist when the task is done
- **Files to create/modify** — exact paths
- **Acceptance criteria** — testable conditions

Do not skip ahead. Later phases assume earlier ones are complete and working.

---

## Phase 1 — Foundation

> Goal: Runnable Django project with auth, custom User model, role system, and base templates.

---

### Task 1.1 — Django Project Scaffolding

**Goal:** A working Django 5.x project structure with all apps registered.

**Steps:**
1. Create Django project named `config` (settings package, not a flat `settings.py`)
2. Create the following Django apps: `accounts`, `tutors`, `guardians`, `requests`, `dashboard`, `core`
3. Register all apps in `INSTALLED_APPS`
4. Configure `TEMPLATES` to include the top-level `templates/` directory
5. Configure `MEDIA_ROOT`, `MEDIA_URL`, `STATIC_ROOT`, `STATIC_URL`
6. Add `python-decouple` and load `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from `.env`
7. Create `.env` file with placeholder values (never commit real secrets)
8. Create `requirements.txt` with all dependencies from Appendix A of the spec

**Files to create:**
```
manage.py
config/__init__.py
config/settings.py
config/urls.py
config/wsgi.py
.env
.env.example
requirements.txt
accounts/__init__.py  (+ apps.py, models.py, views.py, urls.py, forms.py, admin.py)
tutors/__init__.py    (+ apps.py, models.py, views.py, urls.py, forms.py, admin.py)
guardians/__init__.py (+ apps.py, models.py, views.py, urls.py, forms.py, admin.py)
requests/__init__.py  (+ apps.py, models.py, views.py, urls.py, forms.py, admin.py)
dashboard/__init__.py (+ apps.py, views.py, urls.py)
core/__init__.py      (+ apps.py, models.py, utils.py)
```

**Acceptance criteria:**
- `python manage.py check` passes with no errors
- `python manage.py runserver` starts without exceptions

---

### Task 1.2 — Custom User Model

**Goal:** `accounts.User` extends `AbstractUser` with `role`, `phone`, `avatar`, `created_at`.

**Steps:**
1. Implement `User` model in `accounts/models.py` exactly as specified in §5.1
2. Set `AUTH_USER_MODEL = 'accounts.User'` in `settings.py`
3. Create and apply the initial migration (`makemigrations accounts`, `migrate`)
4. Register `User` in `accounts/admin.py` using `UserAdmin` as base

**Files to modify:**
```
accounts/models.py
accounts/admin.py
config/settings.py
```

**Acceptance criteria:**
- Migration runs cleanly
- `User` is visible and functional in Django admin at `/admin/`
- `user.role`, `user.phone`, `user.avatar` fields exist on the model

---

### Task 1.3 — Role-Based Auth: Login / Logout / Register

**Goal:** Working login, logout, and guardian self-registration with role-aware redirects.

**Steps:**
1. Implement `LoginView` at `/login/` — on success redirect to `/dashboard/` 
2. Implement `LogoutView` at `/logout/` — clears session, redirects to `/login/`
3. Implement `RegisterView` at `/register/` — creates a `User` with `role='guardian'`
4. Create `accounts/forms.py` with `LoginForm` and `GuardianRegistrationForm`
5. Create `accounts/decorators.py` with a `role_required(role)` decorator that returns 403 if role doesn't match
6. Wire all URLs through `accounts/urls.py` and include in `config/urls.py`

**Files to create/modify:**
```
accounts/views.py
accounts/forms.py
accounts/urls.py
accounts/decorators.py
config/urls.py
templates/accounts/login.html
templates/accounts/register.html
```

**Acceptance criteria:**
- A new guardian can register, log in, and be redirected to the dashboard
- Logging out clears the session and redirects to `/login/`
- `role_required('admin')` on a view blocks a guardian with HTTP 403

---

### Task 1.4 — Base Templates & Layout Components

**Goal:** A complete base layout (sidebar + topbar) that all pages inherit from.

**Steps:**
1. Create `templates/base.html` with:
   - Tailwind CSS (CDN link)
   - Lucide Icons (CDN link + `lucide.createIcons()` call in a `<script>` at bottom)
   - `{% block content %}{% endblock %}` in the main area
   - `{% include 'components/sidebar.html' %}`
   - `{% include 'components/topbar.html' %}`
2. Create `templates/components/sidebar.html` — navigation links with Lucide icons as per §10 icon table; show/hide links based on `user.role`
3. Create `templates/components/topbar.html` — user avatar, role badge, notification bell with unread count, logout button
4. Create `templates/components/badge.html` — reusable status badge using the Tailwind classes from §10 status badge table; accepts `status` variable
5. Create `templates/components/empty_state.html` — accepts `icon`, `title`, `message` variables
6. Create `templates/components/pagination.html` — standard Django paginator UI
7. Create `templates/errors/404.html` and `templates/errors/500.html`
8. Configure custom error handlers in `config/urls.py`

**Files to create:**
```
templates/base.html
templates/components/sidebar.html
templates/components/topbar.html
templates/components/badge.html
templates/components/empty_state.html
templates/components/pagination.html
templates/errors/404.html
templates/errors/500.html
static/js/app.js       (Lucide init + any UI helpers)
static/css/main.css    (placeholder — Tailwind output)
tailwind.config.js
```

**Acceptance criteria:**
- All pages that extend `base.html` show sidebar and topbar
- Sidebar links are role-filtered (admin sees all, guardian sees subset)
- Lucide icons render correctly in the browser
- Visiting a bad URL shows the custom 404 page

---

### Task 1.5 — Profile View

**Goal:** Logged-in users can view and edit their own profile.

**Steps:**
1. Implement `ProfileView` at `/profile/` (login required)
2. Display: name, email, phone, avatar, role badge
3. Allow editing: name, phone, avatar
4. Use `ModelForm` for the update form

**Files to create/modify:**
```
accounts/views.py
accounts/forms.py
accounts/urls.py
templates/accounts/profile.html
```

**Acceptance criteria:**
- A logged-in user can update their phone number and see the change immediately
- Avatar upload replaces the displayed image

---

## Phase 2 — Core Data Models

> Goal: All domain models created, migrated, and registered in Django admin.

---

### Task 2.1 — Subject Model (core app)

**Goal:** Shared `Subject` model usable across all apps.

**Steps:**
1. Implement `Subject` model in `core/models.py` as per §5.1
2. Create and apply migration
3. Register in `core/admin.py` with list display: `name`, `category`, `is_active`
4. Add `core` to `INSTALLED_APPS` if not already present

**Files to modify:**
```
core/models.py
core/admin.py
```

**Acceptance criteria:**
- Can create subjects via Django admin
- `is_active` filter works in admin

---

### Task 2.2 — TutorProfile Model

**Goal:** `TutorProfile` model linked 1:1 to `User`, with all fields from §5.1.

**Steps:**
1. Implement `TutorProfile` in `tutors/models.py`
2. Define `TUTOR_STATUS` choices: `active`, `inactive`, `suspended`
3. `subjects` is a ManyToManyField to `core.Subject`
4. `availability` is a JSONField
5. Create and apply migration
6. Register in `tutors/admin.py` with inline for subjects

**Files to modify:**
```
tutors/models.py
tutors/admin.py
```

**Acceptance criteria:**
- Can create a `TutorProfile` in Django admin and assign subjects
- `availability` field stores and retrieves JSON correctly

---

### Task 2.3 — GuardianProfile & Student Models

**Goal:** `GuardianProfile` (1:1 User) and `Student` (N:1 GuardianProfile) models.

**Steps:**
1. Implement both models in `guardians/models.py` as per §5.1
2. `Student.subjects_needed` is ManyToManyField to `core.Subject`
3. Create and apply migration
4. Register both in `guardians/admin.py`; use `StudentInline` inside `GuardianProfileAdmin`

**Files to modify:**
```
guardians/models.py
guardians/admin.py
```

**Acceptance criteria:**
- Creating a `GuardianProfile` in admin and adding students inline works
- `Student.subjects_needed` M2M saves correctly

---

### Task 2.4 — TutorRequest Model

**Goal:** `TutorRequest` model with full status pipeline and all FK relationships.

**Steps:**
1. Implement `TutorRequest` in `requests/models.py` as per §5.1
2. Status choices: `pending`, `matched`, `closed`, `cancelled`
3. `assigned_tutor` is nullable FK to `TutorProfile`
4. Create and apply migration
5. Register in `requests/admin.py` with list display: status, guardian, subject, assigned tutor, created_at

**Files to modify:**
```
requests/models.py
requests/admin.py
```

**Acceptance criteria:**
- `TutorRequest` can be created and have a tutor assigned via Django admin
- Status changes save correctly

---

### Task 2.5 — TutorApplication Model

**Goal:** `TutorApplication` model with full status pipeline and file upload fields.

**Steps:**
1. Implement `TutorApplication` in `tutors/models.py` as per §5.1
2. Status choices: `submitted`, `under_review`, `interview`, `approved`, `rejected`
3. `resume` uploads to `resumes/`, `id_document` uploads to `ids/`
4. `reviewed_by` is nullable FK to `User`
5. Create and apply migration
6. Register in `tutors/admin.py`

**Files to modify:**
```
tutors/models.py
tutors/admin.py
```

**Acceptance criteria:**
- Can upload a resume file via Django admin
- `reviewed_by` FK correctly references `accounts.User`

---

### Task 2.6 — Notification Model

**Goal:** `Notification` model for in-app alerts.

**Steps:**
1. Implement `Notification` in `accounts/models.py` as per §5.1
2. Create and apply migration
3. Register in `accounts/admin.py`
4. Create a helper function `notify(recipient, title, message, link='')` in `core/utils.py` that creates a `Notification` instance

**Files to modify:**
```
accounts/models.py
accounts/admin.py
core/utils.py
```

**Acceptance criteria:**
- `notify(user, 'Test', 'Hello')` creates a `Notification` record in the DB
- Notification is visible in Django admin

---

### Task 2.7 — post_save Signals

**Goal:** Auto-create `TutorProfile` or `GuardianProfile` when a `User` is created with the matching role.

**Steps:**
1. Create `accounts/signals.py`
2. On `User` post_save: if `role == 'guardian'`, create `GuardianProfile`; if `role == 'tutor'`, create `TutorProfile`
3. Connect signals in `accounts/apps.py` via `ready()`

**Files to create/modify:**
```
accounts/signals.py
accounts/apps.py
```

**Acceptance criteria:**
- Creating a user with `role='guardian'` in Django admin auto-creates a `GuardianProfile`
- Creating a user with `role='tutor'` auto-creates a `TutorProfile`

---

## Phase 3 — Tutor Application Flow

> Goal: Public `/apply/` form, full admin review pipeline, status transitions.

---

### Task 3.1 — Public Tutor Application Form

**Goal:** Anyone (no login required) can submit a tutor application at `/apply/`.

**Steps:**
1. Create `TutorApplicationCreateView` in `tutors/views.py` — no `login_required`
2. Create `TutorApplicationForm` in `tutors/forms.py` with all fields except status/reviewed_by
3. On valid submission: save with `status='submitted'`, notify all admin users using `core.utils.notify`
4. Redirect to a success page after submission
5. Wire URL `/apply/` in `tutors/urls.py` and include in `config/urls.py`

**Files to create/modify:**
```
tutors/views.py
tutors/forms.py
tutors/urls.py
config/urls.py
templates/tutors/apply.html
templates/tutors/apply_success.html
```

**Acceptance criteria:**
- Submitting the form without logging in creates a `TutorApplication` with status `submitted`
- All admin users receive a `Notification` record
- File upload (resume) works and stores in `media/resumes/`

---

### Task 3.2 — Application List View (Admin)

**Goal:** Admin can see all applications with status filter and pagination.

**Steps:**
1. Create `TutorApplicationListView` at `/admin/applications/` — `role_required('admin')`
2. Paginate 20 items per page
3. Filter by status using query params (`?status=submitted`)
4. Display pipeline summary: count per status stage
5. Use `select_related('reviewed_by')` to avoid N+1

**Files to create/modify:**
```
tutors/views.py
tutors/urls.py
templates/tutors/application_list.html
```

**Acceptance criteria:**
- Non-admin users are blocked (403)
- Filtering by `?status=under_review` shows only matching applications
- Pagination works with 20+ records

---

### Task 3.3 — Application Detail & Status Review (Admin)

**Goal:** Admin can open an application, view uploaded documents, and advance its status.

**Steps:**
1. Create `TutorApplicationDetailView` at `/admin/applications/<id>/` — `role_required('admin')`
2. Display all application fields including document download links
3. Provide a form to update `status` and `reviewer_notes`; auto-set `reviewed_by = request.user`
4. On status change: create `Notification` for the applicant if they have a user account

**Files to create/modify:**
```
tutors/views.py
tutors/urls.py
templates/tutors/application_detail.html
```

**Acceptance criteria:**
- Admin can move status from `submitted` → `under_review` → `interview` → `approved`/`rejected`
- `reviewed_by` is set to the logged-in admin on every status update
- Resume download link works

---

### Task 3.4 — One-Click: Approved Application → Tutor Account

**Goal:** Admin clicks "Create Tutor Account" on an approved application and a `User` + `TutorProfile` is created.

**Steps:**
1. Add a POST action view `approve_to_tutor` at `/admin/applications/<id>/activate/`
2. Only callable when `application.status == 'approved'`
3. Creates `User(role='tutor', email=application.email, ...)` with a random password
4. The `post_save` signal (Task 2.7) auto-creates `TutorProfile`
5. Copies subjects from application to the new `TutorProfile`
6. Displays the generated password on a confirmation page so admin can share it

**Files to create/modify:**
```
tutors/views.py
tutors/urls.py
templates/tutors/tutor_created.html
```

**Acceptance criteria:**
- Clicking the action on an approved application creates both `User` and `TutorProfile`
- Attempting this on a non-approved application returns 400 or redirects with an error message
- Subjects are correctly copied

---

## Phase 4 — Guardian & Request Flow

> Goal: Guardians can manage students and submit/track tutor requests; admins can assign tutors.

---

### Task 4.1 — Guardian Dashboard

**Goal:** Logged-in guardian sees their active requests, linked students, and a "New Request" shortcut.

**Steps:**
1. Implement the `dashboard` view for guardians in `dashboard/views.py`
2. Context: `active_requests` (status=pending/matched), `students`, `recent_notifications`
3. Use `select_related` and `prefetch_related` appropriately

**Files to create/modify:**
```
dashboard/views.py
dashboard/urls.py
templates/dashboard/guardian.html
```

**Acceptance criteria:**
- Guardian sees only their own requests (not other guardians')
- "New Request" button links to `/requests/new/`

---

### Task 4.2 — Student Management (Guardian)

**Goal:** Guardian can add and edit their own students.

**Steps:**
1. Create `StudentCreateView` at `/guardians/students/add/` — `login_required`, guardian only
2. Create `StudentEditView` at `/guardians/students/<id>/edit/` — ownership check (student must belong to this guardian)
3. Create `StudentForm` in `guardians/forms.py`
4. After add/edit, redirect to guardian profile or dashboard

**Files to create/modify:**
```
guardians/views.py
guardians/forms.py
guardians/urls.py
config/urls.py
templates/guardians/student_form.html
```

**Acceptance criteria:**
- Guardian A cannot edit Guardian B's student (returns 403/404)
- Subjects in `subjects_needed` M2M are selectable from active `Subject` records

---

### Task 4.3 — Submit Tutor Request (Guardian)

**Goal:** Guardian submits a tutor request form; admin is notified.

**Steps:**
1. Create `RequestCreateView` at `/requests/new/` — `login_required`, guardian only
2. Create `TutorRequestForm` in `requests/forms.py`; `student` queryset limited to `request.user.guardianprofile.students`
3. On save: `status='pending'`, `guardian=request.user.guardianprofile`
4. Notify all admins via `core.utils.notify`

**Files to create/modify:**
```
requests/views.py
requests/forms.py
requests/urls.py
config/urls.py
templates/requests/request_form.html
```

**Acceptance criteria:**
- Guardian can only select their own students in the dropdown
- Submission creates `TutorRequest` with `status='pending'`
- Admins receive a notification

---

### Task 4.4 — Request List View

**Goal:** Guardians see their own requests; admins see all requests, with filters.

**Steps:**
1. Create `RequestListView` at `/requests/` — `login_required`
2. If `user.role == 'guardian'`: filter by `guardian=user.guardianprofile`
3. If `user.role == 'admin'`: show all, with filter by status, subject, date range
4. Paginate 20 per page; use `select_related('guardian__user', 'subject', 'assigned_tutor__user')`

**Files to create/modify:**
```
requests/views.py
requests/urls.py
templates/requests/request_list.html
```

**Acceptance criteria:**
- Guardian sees only their own requests
- Admin can filter by `?status=pending` and see all matching
- N+1 queries do not occur (verify with Django Debug Toolbar or query count)

---

### Task 4.5 — Request Detail View

**Goal:** Show full request details to the appropriate roles.

**Steps:**
1. Create `RequestDetailView` at `/requests/<id>/` — `login_required`
2. Guardians can only view their own requests
3. Display: all fields, assigned tutor info (if matched), admin notes, status badge

**Files to create/modify:**
```
requests/views.py
requests/urls.py
templates/requests/request_detail.html
```

**Acceptance criteria:**
- Guardian A cannot view Guardian B's request (404)
- Status badge uses the correct Tailwind class from §10

---

### Task 4.6 — Assign Tutor & Update Request (Admin)

**Goal:** Admin can assign a tutor, change status, and add internal notes.

**Steps:**
1. Create `RequestUpdateView` at `/requests/<id>/edit/` — `role_required('admin')`
2. Form fields: `status`, `assigned_tutor`, `admin_notes`
3. `assigned_tutor` queryset: only `TutorProfile` records with `status='active'` and matching subject
4. On save: notify guardian and assigned tutor via `core.utils.notify`

**Files to create/modify:**
```
requests/views.py
requests/forms.py
requests/urls.py
templates/requests/request_update.html
```

**Acceptance criteria:**
- Admin assigns a tutor → status auto-becomes `matched` (or admin sets it manually)
- Both guardian and tutor receive a notification
- Tutor dropdown only shows active tutors

---

### Task 4.7 — Cancel Request (Guardian)

**Goal:** Guardian can cancel their own pending request.

**Steps:**
1. Create `RequestCancelView` at `/requests/<id>/cancel/` — `login_required`, ownership check
2. Only allowed when `status == 'pending'`
3. Sets `status = 'cancelled'`; no tutor notifications needed
4. Confirm via POST (show a confirmation page on GET)

**Files to create/modify:**
```
requests/views.py
requests/urls.py
templates/requests/request_cancel_confirm.html
```

**Acceptance criteria:**
- Cancel only works on pending requests (matched requests cannot be cancelled this way)
- Cancellation is reflected immediately in the request list

---

## Phase 5 — Admin Panel UI

> Goal: Full custom admin dashboard with management views for all entities.

---

### Task 5.1 — Admin Dashboard

**Goal:** Admin lands on a stats dashboard with KPI cards and recent activity.

**Steps:**
1. Implement admin dashboard in `dashboard/views.py`, route `/dashboard/`
2. Context: `total_active_tutors`, `total_guardians`, `open_requests` (pending), `pending_applications`, `recent_activity` (latest 10 objects across requests + applications — combined and sorted by `created_at`/`updated_at`)
3. Quick-action cards: "Review Applications" (→ `/admin/applications/?status=submitted`), "Unassigned Requests" (→ `/requests/?status=pending`)

**Files to create/modify:**
```
dashboard/views.py
templates/dashboard/admin.html
```

**Acceptance criteria:**
- KPI counts are accurate
- Recent activity lists the 10 latest events
- Quick-action links navigate correctly

---

### Task 5.2 — Tutor Directory & Detail (Admin + Guardian)

**Goal:** Paginated, filterable tutor list; full profile detail page.

**Steps:**
1. Create `TutorListView` at `/tutors/` — `login_required` (all roles can view)
2. Filters: subject (dropdown), status (admin only), verified (admin only)
3. Paginate 20/page; use `prefetch_related('subjects')`, `select_related('user')`
4. Create `TutorDetailView` at `/tutors/<id>/` — full profile display
5. Admin sees edit button; tutors see edit button for own profile only

**Files to create/modify:**
```
tutors/views.py
tutors/urls.py
templates/tutors/tutor_list.html
templates/tutors/tutor_detail.html
```

**Acceptance criteria:**
- Filtering by subject shows only tutors with that subject
- Guardian cannot see the edit button on another tutor's profile

---

### Task 5.3 — Tutor Profile Edit (Admin)

**Goal:** Admin can edit any tutor's profile; tutor can edit their own.

**Steps:**
1. Create `TutorEditView` at `/tutors/<id>/edit/` — `login_required`; only admin or the tutor themselves can access
2. Create `TutorProfileForm` in `tutors/forms.py`
3. Form includes: bio, subjects, education_level, experience_yrs, hourly_rate, availability, status (admin only), verified (admin only)

**Files to create/modify:**
```
tutors/views.py
tutors/forms.py
tutors/urls.py
templates/tutors/tutor_edit.html
```

**Acceptance criteria:**
- Tutor editing their own profile cannot change `status` or `verified`
- Admin can set any field

---

### Task 5.4 — Guardian List & Detail (Admin)

**Goal:** Admin can browse guardians and see their students + request history.

**Steps:**
1. Create `GuardianListView` at `/admin/guardians/` — `role_required('admin')`
2. Search by name/email; paginate 20/page
3. Create `GuardianDetailView` at `/admin/guardians/<id>/` — shows profile, all linked students, all submitted requests
4. Include a "Deactivate Account" POST action that sets `user.is_active = False`

**Files to create/modify:**
```
guardians/views.py
guardians/urls.py
config/urls.py
templates/guardians/guardian_list.html
templates/guardians/guardian_detail.html
```

**Acceptance criteria:**
- Search by email partial match works
- Deactivating a guardian prevents them from logging in

---

### Task 5.5 — Create Guardian Account (Admin)

**Goal:** Admin can create guardian accounts directly from the panel.

**Steps:**
1. Add "Add Guardian" form/view at `/admin/guardians/add/` — `role_required('admin')`
2. Form: first name, last name, email, phone, password (set_password)
3. Creates `User(role='guardian')` → signal auto-creates `GuardianProfile`

**Files to create/modify:**
```
guardians/views.py
guardians/urls.py
guardians/forms.py
templates/guardians/guardian_add.html
```

**Acceptance criteria:**
- New guardian can immediately log in with the provided credentials
- `GuardianProfile` exists after account creation

---

### Task 5.6 — Request Kanban / Table Toggle (Admin)

**Goal:** Admin request list has a toggle between table view and a kanban-style status board.

**Steps:**
1. In `RequestListView` (admin context), add a `?view=kanban` query param
2. Kanban: four columns — Pending, Matched, Closed, Cancelled — with cards per request
3. Table: sortable by created_at, status, guardian; filterable by status, subject, date range
4. Add "Export to CSV" button that exports the currently filtered queryset

**Files to create/modify:**
```
requests/views.py
requests/urls.py
templates/requests/request_list.html  (extend with kanban partial)
templates/requests/partials/request_kanban.html
templates/requests/partials/request_table.html
```

**Acceptance criteria:**
- Toggling between views preserves active filters
- CSV export downloads a valid file with all filtered records
- Kanban columns show correct counts

---

### Task 5.7 — Admin User Management

**Goal:** Admin can create new admin users, deactivate accounts, and reassign roles.

**Steps:**
1. Create `AdminUserListView` at `/admin/users/` — `role_required('admin')`
2. Create `AdminUserCreateView` at `/admin/users/add/` — creates `User(role='admin')`
3. `AdminUserEditView` at `/admin/users/<id>/edit/` — can change role, `is_active`
4. Soft-delete: set `is_active=False` (never hard-delete users)

**Files to create/modify:**
```
accounts/views.py
accounts/urls.py
accounts/forms.py
templates/accounts/admin_user_list.html
templates/accounts/admin_user_form.html
```

**Acceptance criteria:**
- Admin can deactivate another admin account
- Deactivated user cannot log in
- Role change from `tutor` to `guardian` reflects immediately

---

## Phase 6 — Notifications & Polish

> Goal: In-app notification system wired up; responsive UI finalized; empty and loading states added.

---

### Task 6.1 — Notification Bell & List

**Goal:** Topbar shows unread notification count; `/notifications/` lists all with mark-as-read.

**Steps:**
1. Create `NotificationListView` at `/notifications/` — `login_required`
2. Display all notifications for `request.user`, newest first
3. Mark all as read on page visit (or per-notification via AJAX/form POST)
4. Unread count in topbar: add a context processor in `accounts/context_processors.py` that injects `unread_notification_count` into every template
5. Register context processor in `settings.py`

**Files to create/modify:**
```
accounts/views.py
accounts/urls.py
accounts/context_processors.py
config/settings.py
templates/accounts/notification_list.html
templates/components/topbar.html  (wire up unread count)
```

**Acceptance criteria:**
- Notification bell shows correct unread count on every page
- Visiting `/notifications/` marks all as read (count becomes 0)

---

### Task 6.2 — Password Change

**Goal:** Logged-in users can change their password.

**Steps:**
1. Create `ChangePasswordView` at `/password/change/` — `login_required`
2. Use Django's built-in `PasswordChangeForm`
3. On success: update session auth hash (so the user isn't logged out) and redirect to profile

**Files to create/modify:**
```
accounts/views.py
accounts/urls.py
templates/accounts/password_change.html
```

**Acceptance criteria:**
- User changes password and remains logged in
- Old password is required; mismatched new passwords show inline errors

---

### Task 6.3 — Empty States

**Goal:** Every list view shows a friendly empty state when there are no records.

**Steps:**
1. Use `templates/components/empty_state.html` (created in Task 1.4)
2. Add empty-state blocks to: request list, tutor list, guardian list, application list, notification list
3. Each instance passes an appropriate Lucide icon name, title, and message

**Files to modify:**
```
templates/requests/request_list.html
templates/tutors/tutor_list.html
templates/guardians/guardian_list.html
templates/tutors/application_list.html
templates/accounts/notification_list.html
```

**Acceptance criteria:**
- Visiting any list view with zero records shows the empty state component (not a blank page)

---

### Task 6.4 — Responsive Polish

**Goal:** All views are fully usable on mobile (≥ 375px width).

**Steps:**
1. Sidebar collapses to a hamburger menu on mobile (`sm` breakpoint)
2. Tables wrap or scroll horizontally on small screens
3. Forms stack vertically on mobile
4. Topbar adapts — notification bell and avatar remain visible

**Files to modify:**
```
templates/base.html
templates/components/sidebar.html
templates/components/topbar.html
static/js/app.js  (hamburger toggle logic)
```

**Acceptance criteria:**
- At 375px width, no horizontal overflow occurs on any page
- Sidebar toggle opens/closes correctly on mobile

---

## Phase 7 — QA & Security Review

> Goal: All permissions verified, queries optimized, security hardened.

---

### Task 7.1 — Role Permission Audit

**Goal:** Every view enforces the role matrix from §8 of the spec exactly.

**Steps:**
1. For each URL in §7, manually verify: unauthenticated access redirects to `/login/`, wrong-role access returns 403
2. Confirm guardian cannot access any `/admin/*` URL
3. Confirm tutor cannot submit a request or view other tutors' edit pages

**Checklist (verify each):**
- [ ] `/admin/applications/` → 403 for guardian and tutor
- [ ] `/admin/guardians/` → 403 for guardian and tutor
- [ ] `/admin/users/` → 403 for guardian and tutor
- [ ] `/requests/new/` → 403 for tutor
- [ ] `/requests/<id>/edit/` → 403 for guardian and tutor
- [ ] `/tutors/<id>/edit/` → 403 for guardian; tutor can only edit own profile
- [ ] `/guardians/students/<id>/edit/` → 403 if student does not belong to this guardian

**Acceptance criteria:**
- All items in the checklist pass

---

### Task 7.2 — Query Optimization

**Goal:** No N+1 queries on any list view.

**Steps:**
1. Add Django Debug Toolbar to development dependencies
2. Check each list view and confirm no repeated queries per row
3. Add missing `select_related` / `prefetch_related` calls where needed
4. Add `db_index=True` on: `TutorRequest.status`, `TutorRequest.created_at`, `TutorApplication.status`, `User.role`

**Files to modify:**
```
requests/models.py
tutors/models.py
accounts/models.py
requests/views.py
tutors/views.py
guardians/views.py
```

**Acceptance criteria:**
- Django Debug Toolbar shows ≤ 10 queries on any list page with 20 records

---

### Task 7.3 — CSRF & XSS Hardening

**Goal:** All POST forms have CSRF token; no unescaped user content rendered.

**Steps:**
1. Confirm every `<form method="post">` includes `{% csrf_token %}`
2. Search all templates for `| safe` or `mark_safe` usage — remove or verify each is sanitized
3. Ensure file upload views validate MIME type (accept only PDF, DOC, DOCX for resumes; common image types for avatars)

**Files to review:**
```
All templates under templates/
accounts/views.py (avatar upload)
tutors/views.py (resume, id_document upload)
```

**Acceptance criteria:**
- No `| safe` on user-supplied data
- Uploading a `.exe` disguised as a PDF is rejected

---

### Task 7.4 — Login Rate Limiting

**Goal:** Brute-force login attempts are blocked after N failures.

**Steps:**
1. Add `django-axes` to `requirements.txt` and `INSTALLED_APPS`
2. Configure in `settings.py`: `AXES_FAILURE_LIMIT = 5`, `AXES_COOLOFF_TIME = 1` (1 hour)
3. Add `axes.backends.AxesStandaloneBackend` to `AUTHENTICATION_BACKENDS`
4. Run `python manage.py migrate` for axes tables

**Files to modify:**
```
requirements.txt
config/settings.py
```

**Acceptance criteria:**
- After 5 failed logins, subsequent attempts are blocked with an error message
- The lockout clears after the cooloff period

---

## Phase 8 — Deployment

> Goal: Production-ready configuration with static files, WSGI server, and hardened settings.

---

### Task 8.1 — Static Files with WhiteNoise

**Goal:** Static files are served correctly without a separate static server.

**Steps:**
1. Add `whitenoise` to `requirements.txt`
2. Add `WhiteNoiseMiddleware` to `MIDDLEWARE` (after `SecurityMiddleware`)
3. Set `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
4. Run `python manage.py collectstatic` and confirm output

**Files to modify:**
```
requirements.txt
config/settings.py
```

**Acceptance criteria:**
- `python manage.py collectstatic` runs without errors
- Static files (CSS, JS) load correctly when `DEBUG=False`

---

### Task 8.2 — Production Settings Hardening

**Goal:** Production `settings.py` is secure and environment-driven.

**Steps:**
1. Ensure all sensitive values come from `.env` via `python-decouple`: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL` (if applicable)
2. Set `SECURE_BROWSER_XSS_FILTER = True`, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF = True`
3. Set `SESSION_COOKIE_HTTPONLY = True`, `CSRF_COOKIE_HTTPONLY = True`
4. Create a `config/settings_prod.py` or use environment variable switching

**Files to modify:**
```
config/settings.py
.env.example
```

**Acceptance criteria:**
- `python manage.py check --deploy` produces no critical warnings

---

### Task 8.3 — Gunicorn Configuration

**Goal:** The app runs under `gunicorn` in production.

**Steps:**
1. Add `gunicorn` to `requirements.txt`
2. Create `gunicorn.conf.py` in the project root with: `workers = 3`, `bind = '0.0.0.0:8000'`, `accesslog = '-'`, `errorlog = '-'`
3. Document the start command: `gunicorn config.wsgi:application -c gunicorn.conf.py`

**Files to create:**
```
gunicorn.conf.py
```

**Acceptance criteria:**
- `gunicorn config.wsgi:application` starts without errors
- The app responds to HTTP requests on port 8000

---

### Task 8.4 — Custom Error Pages in Production

**Goal:** Production 404 and 500 errors show the custom branded pages.

**Steps:**
1. Confirm `templates/errors/404.html` and `500.html` exist (created in Task 1.4)
2. Set `handler404` and `handler500` in `config/urls.py`
3. Test by temporarily raising an exception and visiting a bad URL with `DEBUG=False`

**Files to modify:**
```
config/urls.py
```

**Acceptance criteria:**
- `DEBUG=False` + bad URL → custom 404 page (not Django's yellow debug page)
- `DEBUG=False` + unhandled exception → custom 500 page

---

## Appendix — Task Dependency Map

```
Phase 1 (Foundation)
  └── 1.1 Scaffolding
      └── 1.2 User Model
          └── 1.3 Auth Views
              └── 1.4 Base Templates
                  └── 1.5 Profile View

Phase 2 (Models) — requires Phase 1 complete
  ├── 2.1 Subject
  ├── 2.2 TutorProfile  (requires 2.1)
  ├── 2.3 GuardianProfile + Student  (requires 2.1)
  ├── 2.4 TutorRequest  (requires 2.2, 2.3)
  ├── 2.5 TutorApplication  (requires 2.1)
  ├── 2.6 Notification
  └── 2.7 Signals  (requires 2.2, 2.3)

Phase 3 (Tutor Application) — requires Phase 2 complete
  ├── 3.1 Public Apply Form
  ├── 3.2 Application List
  ├── 3.3 Application Detail & Review
  └── 3.4 Approve → Create Tutor

Phase 4 (Guardian & Requests) — requires Phase 2 complete
  ├── 4.1 Guardian Dashboard
  ├── 4.2 Student Management
  ├── 4.3 Submit Request
  ├── 4.4 Request List
  ├── 4.5 Request Detail
  ├── 4.6 Assign Tutor
  └── 4.7 Cancel Request

Phase 5 (Admin Panel) — requires Phases 3 & 4 complete
  ├── 5.1 Admin Dashboard
  ├── 5.2 Tutor Directory
  ├── 5.3 Tutor Edit
  ├── 5.4 Guardian List & Detail
  ├── 5.5 Create Guardian
  ├── 5.6 Request Kanban/Table
  └── 5.7 Admin User Management

Phase 6 (Notifications & Polish) — requires Phase 5 complete
  ├── 6.1 Notification Bell & List
  ├── 6.2 Password Change
  ├── 6.3 Empty States
  └── 6.4 Responsive Polish

Phase 7 (QA) — requires Phase 6 complete
  ├── 7.1 Permission Audit
  ├── 7.2 Query Optimization
  ├── 7.3 CSRF & XSS
  └── 7.4 Login Rate Limiting

Phase 8 (Deployment) — requires Phase 7 complete
  ├── 8.1 WhiteNoise
  ├── 8.2 Production Settings
  ├── 8.3 Gunicorn
  └── 8.4 Custom Error Pages
```

---

*Generated from: `docs/tutorsync-technical-specification.md` — TMS v1.0*

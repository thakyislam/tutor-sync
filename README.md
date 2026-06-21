# TutorSync

A Django-based Tutor Management System that replaces spreadsheet workflows for managing tutors, guardians, and tutor requests.

## Features

- **Role-based access control** — Three roles: Admin, Tutor, and Guardian, each with tailored dashboards and permissions
- **Tutor application pipeline** — Public application form with admin review/approval workflow
- **Tutor request management** — Guardians submit requests; admins manage them via kanban board or table view with CSV export
- **Student management** — Guardians can add and manage their students
- **In-app notifications** — Real-time notification system for status updates and actions
- **User management** — Admin panel for creating and managing users
- **Login security** — Rate limiting via django-axes (5 attempts, 1hr cooloff)
- **Responsive UI** — Tailwind CSS with a sidebar layout, Lucide icons

## Tech Stack

- **Backend:** Django 6.0, Python 3.13
- **Database:** SQLite
- **Frontend:** Tailwind CSS (CDN), Lucide Icons
- **Auth:** Custom user model with role-based decorators
- **Security:** django-axes, CSRF protection, HSTS (production)
- **Static files:** WhiteNoise
- **Production:** Gunicorn

## Project Structure

```
tutor-sync/
├── accounts/       # User model, auth, notifications, admin user management
├── config/         # Django settings, URLs, WSGI/ASGI
├── core/           # Shared Subject model, notify() helper
├── dashboard/      # Role-dispatched dashboard with stats & KPIs
├── guardians/      # Guardian profiles, student CRUD
├── requests/       # Tutor requests, kanban/table views, CSV export
├── tutors/         # Tutor profiles, application review pipeline
├── templates/      # Base layouts, reusable components
├── static/         # CSS, JS, images
└── media/          # User uploads (avatars, resumes, IDs)
```

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thakyislam/tutor-sync.git
   cd tutor-sync
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

   Generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Set the role to `admin` when prompted.

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## User Roles

| Role | Access |
|------|--------|
| **Admin** | Full access — manage users, review tutor applications, handle requests, view stats |
| **Tutor** | View profile, update details, browse tutor directory |
| **Guardian** | Manage students, create/track tutor requests |

## Production Deployment

```bash
# Set environment variables
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn config.wsgi:application -c gunicorn.conf.py
```

## License

This project is for educational purposes.

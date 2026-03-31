

# 📁 Annotated Directory Tree — Placement Portal

```
placement_portal/
```

Main project root containing configuration, application code, database, and scripts.

---

🧠 10-Second Folder Navigation

| Question          | Folder                   |
| ----------------- | ------------------------ |
| Login issue       | `auth_service.py`        |
| Drive logic       | `drive_service.py`       |
| Application rules | `application_service.py` |
| Page layout       | `templates/`             |
| Database tables   | `models/`                |
| Routes            | `blueprints/`            |
| Auth decorators   | `decorators.py`          |


# 1️⃣ Root Level Files

```
config.py
```

**Purpose**

Application configuration.

**Contains**

* SECRET_KEY
* SQLALCHEMY_DATABASE_URI
* UPLOAD_FOLDER
* SQLALCHEMY_TRACK_MODIFICATIONS

**Why**

Separates **configuration from logic**.

---

```
run.py
```

**Purpose**

Application **entry point**.

**What it does**

* Imports `create_app()` from `app/__init__.py`
* Creates Flask instance
* Starts the server

Run with:

```
python run.py
```

---

```
requirements.txt
```

**Purpose**

Lists all dependencies.

Used by:

```
pip install -r requirements.txt
```

---

```
Project_Structure.txt
```

**Purpose**

Auto-generated file showing the **project directory tree**.

Generated with:

```
tree /F /A > Project_Structure.txt
```

---

# 2️⃣ Main Application Package

```
app/
```

Contains the **entire Flask application logic**.

---

# 3️⃣ Core Application Setup

```
app/__init__.py
```

**Purpose**

Application factory.

**Responsibilities**

* Create Flask app
* Load configuration
* Initialize extensions
* Register blueprints
* Register error handlers

---

```
app/extensions.py
```

**Purpose**

Central location for Flask extensions.

Example:

```
db = SQLAlchemy()
login_manager = LoginManager()
```

Prevents **circular imports**.

---

```
app/decorators.py
```

**Purpose**

Role-based access control.

Contains decorators like:

```
@admin_required
@company_required
@student_required
```

Used to **protect routes**.

---

# 4️⃣ Blueprints (Routes Layer)

```
app/blueprints/
```

Contains **Flask route modules grouped by role**.

```
admin/
auth/
company/
student/
api/
```

Each module contains:

```
routes.py
```

which defines URLs.

Example:

```
/admin/dashboard
/company/create-drive
/student/my-applications
```

---

# 5️⃣ Models (Database Layer)

```
app/models/
```

Defines **SQLAlchemy ORM models**.

Files:

```
user.py
student.py
company.py
placement_drive.py
application.py
notification.py
admin.py
```

Each file defines a **database table**.

Example:

```
User → authentication
Student → student profile
Company → recruiter profile
PlacementDrive → job posting
Application → student applications
```

---

# 6️⃣ Services (Business Logic Layer)

```
app/services/
```

This is where **all business logic lives**.

Files:

```
auth_service.py
approval_service.py
drive_service.py
application_service.py
student_service.py
```

Example responsibilities:

```
auth_service.py
→ login validation
→ password hashing

approval_service.py
→ approve company
→ approve drive

application_service.py
→ apply to drive
→ shortlist candidate
→ select / reject
```

Routes call **services**, not database directly.

Architecture:

```
Route → Service → Model
```

---

# 7️⃣ Templates (Frontend UI)

```
app/templates/
```

Contains **Jinja2 HTML templates**.

Structure:

```
base.html
landing.html
```

Global templates.

---

## Admin Templates

```
templates/admin/
```

Admin interface.

Pages:

```
dashboard.html
pending_companies.html
pending_drives.html
manage_students.html
manage_companies.html
applications.html
reports.html
```

Reusable UI pieces:

```
components/
```

Examples:

```
_admin_sidebar.html
_stats_cards.html
_search_panel.html
_notifications.html
```

---

## Auth Templates

```
templates/auth/
```

Authentication UI.

Files:

```
login.html
register_student.html
register_company.html
```

Components:

```
_login_form.html
_register_student_form.html
_register_company_form.html
```

---

## Company Templates

```
templates/company/
```

Company dashboard pages.

```
dashboard.html
create_drive.html
my_drives.html
drive_detail.html
applications.html
shortlisted_candidates.html
profile.html
```

Components:

```
_company_sidebar.html
_company_profile_card.html
_stats_cards.html
_notifications.html
```

---

## Student Templates

```
templates/student/
```

Student dashboard.

Files:

```
dashboard.html
my_applications.html
placement_history.html
profile.html
```

Components:

```
_student_sidebar.html
_drive_table.html
_profile_snapshot.html
_stats_cards.html
_notifications.html
```

---

# 8️⃣ Static Files

```
app/static/
```

Frontend assets.

```
css/
images/
```

CSS example:

```
style.css
admin_layout.css
admin_cards.css
admin_forms.css
```

Used to style the UI.

---

# 9️⃣ File Uploads

```
app/uploads/resumes/
```

Stores uploaded student resumes.

Example:

```
23bcsg60_resume.pdf
```

Used during job applications.

---

# 🔟 Utilities

```
app/utils/
```

Helper modules.

```
constants.py
validators.py
```

Examples:

```
APPLICATION_APPLIED
DRIVE_APPROVED
COMPANY_PENDING
```

Prevents hardcoding strings.

---

# 1️⃣1️⃣ Error Handlers

```
app/errors/
```

Handles HTTP errors.

Example:

```
404 → page not found
403 → forbidden
500 → server error
```

File:

```
handlers.py
```

---

# 1️⃣2️⃣ Instance Folder

```
instance/
```

Contains runtime data.

```
placement.db
```

SQLite database file.

Kept outside app to **avoid accidental commits**.

---

# 1️⃣3️⃣ Scripts

```
scripts/
```

Utility scripts.

Example:

```
seed_admin.py
```

Creates default admin user.

Run once:

```
python scripts/seed_admin.py
```

---

# 🧠 Full Architecture in One Line

```
User Request
   ↓
Blueprint Route
   ↓
Service Layer
   ↓
SQLAlchemy Model
   ↓
Database
   ↓
Template Rendering
   ↓
HTML Response
```

---


> The project follows a modular Flask architecture using blueprints for routing, services for business logic, SQLAlchemy models for database interaction, and Jinja templates for the user interface.


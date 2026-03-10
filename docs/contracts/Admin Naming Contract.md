**ADMIN MODULE NAMING CONTRACT**.

This document defines:

* Model references
* Service method names
* Route names
* URL patterns
* Template file names
* Template variable contracts
* Allowed state transitions
* Search parameter naming
* Blacklist rules

This is now the **authoritative standard** for anything inside:

```
app/blueprints/admin/
templates/admin/
services/approval_service.py
```

---

# 📘 ADMIN MODULE NAMING CONTRACT

Version 1.0 – Authoritative

---

# 1️⃣ ADMIN ROLE DEFINITION

## 1.1 Role Constant

Must use:

```python
ADMIN = "admin"
```

Never compare `"Admin"` or `"ADMIN"`.

---

## 1.2 Admin Model

### Class Name

```python
class Admin(db.Model)
```

### Table Name

```
admins
```

### Foreign Key

```
user_id
```

Admin must always be linked to `users.id`.

---

# 2️⃣ ADMIN BLUEPRINT CONTRACT

## 2.1 Blueprint Name

```python
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
```

Blueprint name: `"admin"`
URL prefix: `/admin`

Never change this.

---

## 2.2 URL Naming Rules

Use kebab-case in URLs.

Correct:

```
/admin/dashboard
/admin/pending-companies
/admin/pending-drives
/admin/manage-students
/admin/manage-companies
/admin/applications
/admin/reports
```

Never:

```
/admin/manageStudents
/admin/pending_drives
```

---

# 3️⃣ ADMIN ROUTE FUNCTION NAMING

All route functions must end with `_view`.

Pattern:

```
<action>_<entity>_view
```

---

## 3.1 Dashboard

```python
admin_dashboard_view()
```

URL:

```
/admin/dashboard
```

---

## 3.2 Company Approval

```python
pending_companies_view()
approve_company_view(company_id)
reject_company_view(company_id)
```

URLs:

```
/admin/pending-companies
/admin/approve-company/<int:company_id>
/admin/reject-company/<int:company_id>
```

---

## 3.3 Drive Approval

```python
pending_drives_view()
approve_drive_view(drive_id)
reject_drive_view(drive_id)
```

URLs:

```
/admin/pending-drives
/admin/approve-drive/<int:drive_id>
/admin/reject-drive/<int:drive_id>
```

---

## 3.4 Student Management

```python
manage_students_view()
blacklist_student_view(student_id)
activate_student_view(student_id)
```

URLs:

```
/admin/manage-students
/admin/blacklist-student/<int:student_id>
/admin/activate-student/<int:student_id>
```

---

## 3.5 Company Management

```python
manage_companies_view()
blacklist_company_view(company_id)
activate_company_view(company_id)
```

---

## 3.6 Applications View

```python
view_all_applications_view()
```

URL:

```
/admin/applications
```

---

## 3.7 Reports

```python
reports_view()
```

URL:

```
/admin/reports
```

---

# 4️⃣ ADMIN SERVICE CONTRACT

Admin must NEVER access database directly inside routes.

Routes call services only.

---

## 4.1 Approval Service Methods

Located in:

```
services/approval_service.py
```

Required methods:

```python
approve_company(company_id)
reject_company(company_id)

approve_drive(drive_id)
reject_drive(drive_id)
```

---

## 4.2 Admin Management Service Methods

Either inside `approval_service.py` or `admin_service.py`.

```python
blacklist_student(student_id)
activate_student(student_id)

blacklist_company(company_id)
activate_company(company_id)

get_admin_dashboard_stats()
get_all_applications()
search_students(query)
search_companies(query)
```

All names must be verbs.

---

# 5️⃣ ADMIN TEMPLATE CONTRACT

Templates must live inside:

```
templates/admin/
```

---

## 5.1 File Naming

Exact names:

```
dashboard.html
pending_companies.html
pending_drives.html
manage_students.html
manage_companies.html
applications.html
reports.html
```

Partials:

```
_admin_sidebar.html
_stats_cards.html
_search_panel.html
_notifications.html
```

Prefix `_` required for partials.

---

# 6️⃣ ADMIN PAGE DATA CONTRACTS

These are mandatory.

---

## 6.1 Dashboard Contract

Route must pass:

```python
{
    "total_students": int,
    "total_companies": int,
    "total_drives": int,
    "total_applications": int
}
```

Template must use:

```
{{ total_students }}
{{ total_companies }}
{{ total_drives }}
{{ total_applications }}
```

Never use camelCase.

---

## 6.2 Pending Companies Contract

```python
{
    "pending_companies": list[Company]
}
```

Template usage:

```
{% for company in pending_companies %}
    {{ company.company_name }}
    {{ company.approval_status }}
{% endfor %}
```

---

## 6.3 Pending Drives Contract

```python
{
    "pending_drives": list[PlacementDrive]
}
```

---

## 6.4 Manage Students Contract

```python
{
    "students": list[Student]
}
```

Student model must expose:

```
student.id
student.student_id
student.name
student.branch
student.cgpa
student.is_blacklisted
```

---

## 6.5 Manage Companies Contract

```python
{
    "companies": list[Company]
}
```

---

## 6.6 Applications Contract

```python
{
    "applications": list[Application]
}
```

Application template fields:

```
application.student
application.drive
application.status
application.applied_at
```

---

## 6.7 Reports Contract

```python
{
    "total_selected": int,
    "total_rejected": int,
    "selection_ratio": float
}
```

---

# 7️⃣ SEARCH PARAMETER CONTRACT

Query parameter name must always be:

```
q
```

Example:

```
/admin/manage-students?q=aman
```

Route receives:

```python
query = request.args.get("q")
```

Never use:

```
search
keyword
text
```

Standardize to `q`.

---

# 8️⃣ STATUS TRANSITION RULES (Admin-Controlled)

Admin can change:

### Company

```
pending → approved
pending → rejected
```

Admin cannot:

```
approved → pending
```

---

### Drive

```
pending → approved
pending → rejected
```

Admin cannot modify:

```
approved → closed
```

Closing drive belongs to Company.

---

# 9️⃣ BLACKLIST RULES

Boolean field:

```
is_blacklisted
```

Admin methods:

```python
blacklist_student(student_id)
activate_student(student_id)
```

Never:

```
remove_student()
disable_student()
```

Use consistent vocabulary: **blacklist / activate**

---

# 🔟 STRICTLY FORBIDDEN

❌ DB queries inside route
❌ Template checking roles
❌ Hardcoded status strings
❌ Mixed snake_case & camelCase
❌ Different variable names for same concept

---

# 1️⃣1️⃣ ADMIN MODULE FLOW GUARANTEE

Correct flow:

```
Route (admin/routes.py)
    ↓
Service (approval_service.py / admin_service.py)
    ↓
Model (SQLAlchemy)
    ↓
Return clean contract dict
    ↓
Template
```

No deviation allowed.

---

# 🧠 What This Prevents

* Naming mismatch
* Status inconsistency
* Refactoring cascade
* Template confusion
* Future MERN migration difficulty

---


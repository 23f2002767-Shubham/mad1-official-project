 **strict Naming Contract Document** for the Institute Placement Portal Project

This document becomes your **law**.
If something violates this → it gets refactored.

This is designed to match your existing modular structure  and lifecycle logic .

---

# 📘 PLACEMENT PORTAL — NAMING CONTRACT DOCUMENT

Version 1.0 (Authoritative Standard)

---

# 1️⃣ GLOBAL RULES (Applies Everywhere)

## 1.1 Case Style Rules

| Layer           | Convention              |
| --------------- | ----------------------- |
| Python files    | snake_case              |
| Classes         | PascalCase              |
| Variables       | snake_case              |
| Functions       | snake_case (verb-based) |
| Database tables | plural, snake_case      |
| Columns         | snake_case              |
| HTML templates  | snake_case              |
| URL paths       | kebab-case              |
| Blueprint names | singular                |

---

## 1.2 Core Vocabulary (Single Source of Truth)

These names MUST NEVER vary.

### Roles

```python
ADMIN = "admin"
COMPANY = "company"
STUDENT = "student"
```

### Company Approval Status

```python
COMPANY_PENDING = "pending"
COMPANY_APPROVED = "approved"
COMPANY_REJECTED = "rejected"
```

### Drive Status

```python
DRIVE_PENDING = "pending"
DRIVE_APPROVED = "approved"
DRIVE_CLOSED = "closed"
```

### Application Status

```python
APPLICATION_APPLIED = "applied"
APPLICATION_SHORTLISTED = "shortlisted"
APPLICATION_SELECTED = "selected"
APPLICATION_REJECTED = "rejected"
```

These must live inside:

```
app/utils/constants.py
```

No hardcoded strings allowed anywhere else.

---

# 2️⃣ MODEL NAMING CONTRACT

## 2.1 Table Naming

| Model Class    | **tablename**    |
| -------------- | ---------------- |
| User           | users            |
| Admin          | admins           |
| Company        | companies        |
| Student        | students         |
| PlacementDrive | placement_drives |
| Application    | applications     |
| Notification   | notifications    |

Plural. snake_case. Always.

---

## 2.2 Column Naming Rules

### Primary Key

```python
id = db.Column(db.Integer, primary_key=True)
```

Always `id`. Never `user_id` as primary key.

---

### Foreign Keys

| Relationship          | Column     |
| --------------------- | ---------- |
| Company → User        | user_id    |
| Student → User        | user_id    |
| Drive → Company       | company_id |
| Application → Student | student_id |
| Application → Drive   | drive_id   |

Pattern:

```
<related_entity>_id
```

---

## 2.3 Boolean Fields

Must start with `is_`

Examples:

```python
is_active
is_blacklisted
is_resume_uploaded
```

Never:

```
active
blacklist
resumeUploaded
```

---

## 2.4 Date/Time Fields

Use suffixes:

| Type      | Naming |
| --------- | ------ |
| Date      | *_date |
| Timestamp | *_at   |

Examples:

```
application_deadline
applied_at
approved_at
created_at
```

Never mix `_date` and `_at` randomly.

---

# 3️⃣ SERVICE LAYER NAMING CONTRACT

Services represent **business actions**.

Pattern:

```
<entity>_service.py
```

Examples:

```
auth_service.py
approval_service.py
application_service.py
drive_service.py
```

---

## 3.1 Function Naming Rules

Functions must be verbs.

### Admin Services

```python
approve_company(company_id)
reject_company(company_id)
approve_drive(drive_id)
reject_drive(drive_id)
blacklist_student(student_id)
blacklist_company(company_id)
get_admin_dashboard_stats()
```

---

### Company Services

```python
create_drive(company_id, form_data)
update_drive(drive_id, form_data)
close_drive(drive_id)
get_company_dashboard_stats(company_id)
get_drive_applications(drive_id)
shortlist_application(application_id)
select_application(application_id)
reject_application(application_id)
```

---

### Student Services

```python
register_student(form_data)
update_student_profile(student_id, form_data)
upload_resume(student_id, file)
apply_to_drive(student_id, drive_id)
get_student_dashboard_data(student_id)
get_student_applications(student_id)
```

---

## 3.2 Service Return Contract Rule

Services must return:

* Model object
* Boolean
* Dict (clear keys only)

Never return:

```
data
obj
result
response
```

Return explicit shape:

```python
{
    "total_students": int,
    "total_companies": int,
    "total_drives": int,
    "total_applications": int
}
```

---

# 4️⃣ BLUEPRINT ROUTE NAMING CONTRACT

Folder:

```
app/blueprints/
```

Blueprint names:

```python
admin_bp
company_bp
student_bp
auth_bp
```

---

## 4.1 URL Pattern Rules

| Role    | Prefix   |
| ------- | -------- |
| Admin   | /admin   |
| Company | /company |
| Student | /student |
| Auth    | /auth    |

---

## 4.2 URL Style

Use kebab-case:

Correct:

```
/admin/manage-students
/company/create-drive
/student/my-applications
```

Never:

```
/admin/manageStudents
/company/create_drive
```

---

## 4.3 Route Function Naming

Pattern:

```
<action>_<entity>_view
```

Examples:

```python
admin_dashboard_view()
approve_company_view(company_id)
manage_students_view()
create_drive_view()
apply_to_drive_view(drive_id)
```

Suffix `_view` for clarity.

---

# 5️⃣ TEMPLATE NAMING CONTRACT

Templates live in:

```
templates/admin/
templates/company/
templates/student/
```

---

## 5.1 File Naming

snake_case only.

Examples:

### Admin

```
dashboard.html
pending_companies.html
pending_drives.html
manage_students.html
manage_companies.html
applications.html
reports.html
```

### Company

```
dashboard.html
create_drive.html
my_drives.html
drive_detail.html
applications.html
shortlisted_candidates.html
profile.html
```

### Student

```
dashboard.html
available_drives.html
my_applications.html
placement_history.html
profile.html
upload_resume.html
```

---

## 5.2 Partial Templates

Prefix with `_`

Examples:

```
_stats_cards.html
_sidebar.html
_notifications.html
```

---

## 5.3 Template Variable Naming Rules

Must match backend variable names exactly.

Correct:

```jinja
{{ total_students }}
{{ drive.job_title }}
{{ application.status }}
```

Never:

```jinja
{{ totalStudents }}
{{ driveTitle }}
{{ appStatus }}
```

---

# 6️⃣ DATA CONTRACT PER PAGE (CRITICAL)

Before writing template, define contract.

---

## Admin Dashboard Contract

```python
{
    "total_students": int,
    "total_companies": int,
    "total_drives": int,
    "total_applications": int,
}
```

---

## Company Dashboard Contract

```python
{
    "company": Company,
    "total_drives": int,
    "total_applicants": int,
    "recent_drives": list[PlacementDrive]
}
```

---

## Student Dashboard Contract

```python
{
    "student": Student,
    "available_drives": list[PlacementDrive],
    "recent_applications": list[Application]
}
```

---

# 7️⃣ STATUS TRANSITION RULES (Must Match Lifecycle)

Based on lifecycle document 

Valid transitions:

### Application

```
applied → shortlisted
shortlisted → selected
shortlisted → rejected
```

Direct:

```
applied → selected ❌ (Not allowed)
```

Enforce inside service only.

---

# 8️⃣ WHAT IS FORBIDDEN

❌ Hardcoded status strings
❌ Business logic in templates
❌ Role checks inside HTML
❌ Mixed camelCase and snake_case
❌ Routes performing DB queries directly
❌ Duplicate naming for same concept

---

# 9️⃣ MIGRATION READINESS GUARANTEE

If this contract is followed:

* Flask → Express migration becomes syntax-only
* Jinja → React migration becomes rendering-only
* Business logic untouched

Matches migration checklist principles .

---

# 🔟 FINAL ENGINEERING RULE

When adding any feature:

1. Update constants first
2. Update model (if needed)
3. Write service method
4. Define return contract
5. Write route
6. Then write template

Never reverse the order.

---

# 🧠 What This Document Gives You

* No more naming mismatch
* No more “why is this variable different?”
* Clear mental map
* Migration safety
* Industry-level structure

---


**STUDENT MODULE NAMING CONTRACT**.

This document governs everything inside:

```
app/blueprints/student/
templates/student/
services/application_service.py
services/student_service.py
```

This is the authoritative naming and responsibility standard for the Student module.

---

# 📘 STUDENT MODULE NAMING CONTRACT

Version 1.0 – Authoritative

---

# 1️⃣ STUDENT ROLE DEFINITION

## 1.1 Role Constant

Must use:

```python
STUDENT = "student"
```

Never:

* `"Student"`
* `"std"`
* `"student_user"`

---

# 2️⃣ STUDENT MODEL CONTRACT

## 2.1 Class Name

```python
class Student(db.Model)
```

## 2.2 Table Name

```
students
```

Plural. snake_case. Never `student_table`.

---

## 2.3 Required Fields

These field names are fixed:

```python
id
user_id
student_id
name
branch
cgpa
resume_path
is_resume_uploaded
is_blacklisted
created_at
```

---

## 2.4 Naming Rules

### Boolean fields must start with:

```
is_
```

Correct:

```
is_resume_uploaded
is_blacklisted
```

Never:

```
resumeUploaded
blacklist
active
```

---

## 2.5 Foreign Key

```
user_id
```

Always link to `users.id`.

---

# 3️⃣ STUDENT BLUEPRINT CONTRACT

## 3.1 Blueprint Definition

```python
student_bp = Blueprint("student", __name__, url_prefix="/student")
```

Blueprint name: `"student"`
URL prefix: `/student`

---

## 3.2 URL Naming Rules

Use kebab-case only.

Correct:

```
/student/dashboard
/student/available-drives
/student/my-applications
/student/placement-history
/student/profile
/student/upload-resume
/student/apply/<int:drive_id>
```

Never:

```
/student/myApplications
/student/upload_resume
```

---

# 4️⃣ STUDENT ROUTE FUNCTION NAMING

All route functions must end with `_view`.

Pattern:

```
<action>_<entity>_view
```

---

## 4.1 Dashboard

```python
student_dashboard_view()
```

---

## 4.2 Drives

```python
available_drives_view()
apply_to_drive_view(drive_id)
```

---

## 4.3 Applications

```python
my_applications_view()
```

---

## 4.4 Placement History

```python
placement_history_view()
```

---

## 4.5 Profile

```python
student_profile_view()
update_student_profile_view()
upload_resume_view()
```

---

# 5️⃣ STUDENT SERVICE CONTRACT

Routes must never contain business logic.

Services must handle:

* Eligibility checks
* Resume validation
* Duplicate application prevention
* Blacklist checks

---

## 5.1 Student Service Methods

Located in:

```
services/student_service.py
```

Required methods:

```python
register_student(form_data)
update_student_profile(student_id, form_data)
upload_resume(student_id, file)
get_student_dashboard_data(student_id)
get_available_drives(student_id)
```

---

## 5.2 Application Service (Student Side)

Located in:

```
services/application_service.py
```

Required methods:

```python
apply_to_drive(student_id, drive_id)
get_student_applications(student_id)
get_student_placement_history(student_id)
```

---

# 6️⃣ APPLICATION RULES (Student-Controlled)

Student can only:

```
create application → status = applied
```

Student cannot:

```
shortlist
select
reject
delete application
change status
```

Enforcement must exist inside `application_service.py`.

---

# 7️⃣ TEMPLATE CONTRACT

Templates must live inside:

```
templates/student/
```

---

## 7.1 Required Files

```
dashboard.html
available_drives.html
my_applications.html
placement_history.html
profile.html
upload_resume.html
```

Partials:

```
_student_sidebar.html
_stats_cards.html
_drive_table.html
_profile_snapshot.html
_notifications.html
```

Prefix `_` required for partials.

---

# 8️⃣ PAGE DATA CONTRACTS

These contracts must be respected strictly.

---

## 8.1 Dashboard Contract

Route must pass:

```python
{
    "student": Student,
    "available_drives_count": int,
    "applied_drives_count": int,
    "selected_count": int,
    "recent_applications": list[Application]
}
```

Template must use:

```
{{ student.name }}
{{ available_drives_count }}
{{ applied_drives_count }}
{{ selected_count }}
```

Never:

```
studentName
driveCount
```

---

## 8.2 Available Drives Contract

```python
{
    "available_drives": list[PlacementDrive]
}
```

Template:

```
{% for drive in available_drives %}
    {{ drive.job_title }}
    {{ drive.company.company_name }}
    {{ drive.application_deadline }}
{% endfor %}
```

---

## 8.3 Apply Button Rule

Template must NOT check eligibility logic.

Service must compute eligibility.

If needed, pass:

```python
{
    "can_apply": bool
}
```

Never compute in template.

---

## 8.4 My Applications Contract

```python
{
    "applications": list[Application]
}
```

Template fields:

```
{{ application.drive.job_title }}
{{ application.status }}
{{ application.applied_at }}
```

---

## 8.5 Placement History Contract

```python
{
    "placement_history": list[Application]
}
```

Filter only:

```
status == selected
```

This filtering must happen in service.

---

## 8.6 Profile Contract

```python
{
    "student": Student
}
```

Editable fields:

```
name
branch
cgpa
```

Never editable:

```
student_id
is_blacklisted
```

---

# 9️⃣ RESUME CONTRACT

Upload route:

```python
upload_resume_view()
```

Service method:

```python
upload_resume(student_id, file)
```

Stored as:

```
resume_path
is_resume_uploaded = True
```

File types allowed:

```
pdf
doc
docx
```

Validation must be in service or validator.

---

# 🔟 SEARCH PARAMETER RULE

If search exists:

Query parameter must be:

```
q
```

Example:

```
/student/available-drives?q=backend
```

---

# 1️⃣1️⃣ STATUS USAGE RULE

Student can only see:

```
applied
shortlisted
selected
rejected
```

Never hardcode strings in template.

Use constants from:

```
app/utils/constants.py
```

---

# 1️⃣2️⃣ PERMISSION RULES

Student cannot:

* Access admin routes
* Access company routes
* View other students’ data
* Apply if blacklisted
* Apply without resume
* Apply twice to same drive

All enforcement must exist in services.

---

# 1️⃣3️⃣ STUDENT MODULE FLOW GUARANTEE

Correct flow:

```
Route (student/routes.py)
    ↓
Service (student_service / application_service)
    ↓
Model (SQLAlchemy)
    ↓
Return explicit contract dict
    ↓
Template
```

No deviation allowed.

---

# 🧠 What This Prevents

* Duplicate applications
* Resume-related bugs
* Naming mismatches
* Template logic abuse
* Security leaks
* Hardcoded status chaos

---



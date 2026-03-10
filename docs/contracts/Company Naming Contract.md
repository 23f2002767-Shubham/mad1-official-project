**COMPANY MODULE NAMING CONTRACT**.

This defines the authoritative rules for everything inside:

```
app/blueprints/company/
templates/company/
services/drive_service.py
services/application_service.py
```

If anything violates this document → it gets refactored.

---

# 📘 COMPANY MODULE NAMING CONTRACT

Version 1.0 – Authoritative

---

# 1️⃣ COMPANY ROLE DEFINITION

## 1.1 Role Constant

Must use:

```python
COMPANY = "company"
```

Never:

* `"Company"`
* `"COMP"`
* `"company_user"`

---

## 1.2 Company Model

### Class Name

```python
class Company(db.Model)
```

### Table Name

```text
companies
```

### Foreign Key

```text
user_id
```

Company must always be linked to `users.id`.

---

## 1.3 Required Company Fields

Must use these exact names:

```python
id
company_name
hr_email
website
approval_status
is_blacklisted
created_at
approved_at
```

Never:

* `companyName`
* `hrEmail`
* `approvedDate`
* `active`

---

# 2️⃣ COMPANY BLUEPRINT CONTRACT

## 2.1 Blueprint Name

```python
company_bp = Blueprint("company", __name__, url_prefix="/company")
```

Blueprint name: `"company"`
URL prefix: `/company`

---

## 2.2 URL Naming Rules

Use kebab-case.

Correct:

```
/company/dashboard
/company/create-drive
/company/my-drives
/company/drive/<int:drive_id>
/company/applications/<int:drive_id>
/company/shortlisted/<int:drive_id>
/company/profile
```

Never:

```
/company/myDrives
/company/create_drive
```

---

# 3️⃣ COMPANY ROUTE FUNCTION NAMING

All route functions must end with `_view`.

Pattern:

```
<action>_<entity>_view
```

---

## 3.1 Dashboard

```python
company_dashboard_view()
```

URL:

```
/company/dashboard
```

---

## 3.2 Drive Management

```python
create_drive_view()
edit_drive_view(drive_id)
close_drive_view(drive_id)
delete_drive_view(drive_id)
my_drives_view()
drive_detail_view(drive_id)
```

---

## 3.3 Applications

```python
view_drive_applications_view(drive_id)
shortlisted_candidates_view(drive_id)
```

---

## 3.4 Application Status Actions

```python
shortlist_application_view(application_id)
select_application_view(application_id)
reject_application_view(application_id)
```

Never:

* `update_status_view`
* `change_application_view`

Be explicit.

---

# 4️⃣ COMPANY SERVICE CONTRACT

Routes must never contain business logic.

All logic lives in:

```text
services/drive_service.py
services/application_service.py
```

---

# 4.1 Drive Service Methods

```python
create_drive(company_id, form_data)
update_drive(drive_id, form_data)
close_drive(drive_id)
delete_drive(drive_id)
get_company_drives(company_id)
get_drive_by_id(drive_id)
get_company_dashboard_stats(company_id)
```

---

# 4.2 Application Service Methods (Company-Side)

```python
get_drive_applications(drive_id)
shortlist_application(application_id)
select_application(application_id)
reject_application(application_id)
```

---

# 4.3 Service Return Contracts

Services must return:

* Model instance
* Boolean
* Explicit dictionary

Never:

* `data`
* `result`
* `response`

Example dashboard contract:

```python
{
    "company": Company,
    "total_drives": int,
    "total_applications": int,
    "recent_drives": list[PlacementDrive]
}
```

---

# 5️⃣ PLACEMENT DRIVE MODEL CONTRACT

## 5.1 Model Class

```python
class PlacementDrive(db.Model)
```

## 5.2 Table Name

```
placement_drives
```

## 5.3 Required Fields

```python
id
company_id
job_title
job_description
eligibility_criteria
application_deadline
status
created_at
approved_at
```

Never:

* `title`
* `description`
* `deadline`
* `driveStatus`

Be explicit.

---

# 6️⃣ APPLICATION STATUS TRANSITION RULES (Company-Controlled)

Valid transitions:

```
applied → shortlisted
shortlisted → selected
shortlisted → rejected
```

Invalid:

```
applied → selected ❌
selected → rejected ❌
rejected → selected ❌
```

These rules must be enforced in `application_service.py`.

Routes must not enforce transitions.

---

# 7️⃣ COMPANY TEMPLATE CONTRACT

Templates must live in:

```
templates/company/
```

---

## 7.1 Required Files

```
dashboard.html
create_drive.html
my_drives.html
drive_detail.html
applications.html
shortlisted_candidates.html
profile.html
```

Partials:

```
_company_sidebar.html
_stats_cards.html
_notifications.html
_company_profile_card.html
```

---

# 8️⃣ TEMPLATE VARIABLE CONTRACTS

## 8.1 Dashboard Contract

Route must pass:

```python
{
    "company": Company,
    "total_drives": int,
    "total_applications": int,
    "recent_drives": list[PlacementDrive]
}
```

Template must use:

```
{{ company.company_name }}
{{ total_drives }}
{{ total_applications }}
```

Never:

* `companyName`
* `driveCount`

---

## 8.2 My Drives Contract

```python
{
    "drives": list[PlacementDrive]
}
```

Template usage:

```
{% for drive in drives %}
    {{ drive.job_title }}
    {{ drive.status }}
{% endfor %}
```

---

## 8.3 Drive Detail Contract

```python
{
    "drive": PlacementDrive,
    "applications_count": int
}
```

---

## 8.4 Applications Contract

```python
{
    "drive": PlacementDrive,
    "applications": list[Application]
}
```

Template fields:

```
{{ application.student.name }}
{{ application.status }}
{{ application.applied_at }}
```

---

## 8.5 Shortlisted Candidates Contract

```python
{
    "drive": PlacementDrive,
    "shortlisted_applications": list[Application]
}
```

---

# 9️⃣ PROFILE CONTRACT

Route:

```python
company_profile_view()
update_company_profile_view()
```

Template contract:

```python
{
    "company": Company
}
```

Editable fields:

```
company_name
hr_email
website
```

Never allow:

```
approval_status
is_blacklisted
```

Those are admin-controlled.

---

# 🔟 PERMISSION RULES

Company cannot:

* Approve itself
* Approve drives
* Access other companies’ drives
* Access applications of other companies
* Remove student applications

All enforcement must happen in services.

---

# 1️⃣1️⃣ SEARCH PARAMETER RULE

If search exists:

Query parameter name must be:

```
q
```

Example:

```
/company/my-drives?q=backend
```

---

# 1️⃣2️⃣ STRICTLY FORBIDDEN

❌ Business logic in templates
❌ Role checks inside HTML
❌ Hardcoded status strings
❌ CamelCase variables
❌ Drive closing handled by admin
❌ Generic route names like `update_view`

---

# 1️⃣3️⃣ COMPANY MODULE FLOW GUARANTEE

Correct flow:

```
Route (company/routes.py)
    ↓
Service (drive_service / application_service)
    ↓
Model (SQLAlchemy)
    ↓
Return explicit contract dict
    ↓
Template
```

---

# 🧠 What This Prevents

* Drive status confusion
* Application transition bugs
* Cross-company data leakage
* Naming mismatches in templates
* Refactor chaos

---


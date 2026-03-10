**AUTH MODULE NAMING CONTRACT**.

This governs everything inside:

```
app/blueprints/auth/
templates/auth/
services/auth_service.py
```

Auth is small but extremely sensitive.
If naming is inconsistent here, your entire app becomes unstable.

This contract enforces:

* Role consistency
* Payload consistency
* Session behavior
* Redirect discipline
* Registration rules

---

# 📘 AUTH MODULE NAMING CONTRACT

Version 1.0 – Authoritative

---

# 1️⃣ AUTH RESPONSIBILITY BOUNDARY

Auth module is responsible ONLY for:

* Login
* Logout
* Registration (student & company)
* Password hashing
* Role assignment
* Session management

Auth module must NOT:

* Approve companies
* Create drives
* Apply to drives
* Enforce business workflows

Auth handles identity.
Other modules handle behavior.

---

# 2️⃣ USER MODEL CONTRACT

## 2.1 Class Name

```python
class User(db.Model)
```

## 2.2 Table Name

```
users
```

Plural. snake_case.

---

## 2.3 Required Fields

```python
id
email
password_hash
role
is_active
created_at
```

Never:

* `username`
* `password`
* `userType`
* `active`

---

## 2.4 Role Values (Must Match Global Constants)

```python
ADMIN = "admin"
COMPANY = "company"
STUDENT = "student"
```

Never compare raw strings inside routes.

---

# 3️⃣ AUTH BLUEPRINT CONTRACT

## 3.1 Blueprint Definition

```python
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
```

Blueprint name: `"auth"`
URL prefix: `/auth`

---

## 3.2 URL Naming Rules

Use kebab-case only.

Correct:

```
/auth/login
/auth/logout
/auth/register-student
/auth/register-company
```

Never:

```
/auth/registerStudent
/auth/register_company
```

---

# 4️⃣ ROUTE FUNCTION NAMING

All route functions must end with `_view`.

Pattern:

```
<action>_<entity>_view
```

---

## 4.1 Login

```python
login_view()
```

URL:

```
/auth/login
```

---

## 4.2 Logout

```python
logout_view()
```

---

## 4.3 Registration

```python
register_student_view()
register_company_view()
```

Never use generic:

```
register_view()
```

Be explicit.

---

# 5️⃣ AUTH SERVICE CONTRACT

Located in:

```
services/auth_service.py
```

Routes must NOT:

* Query database directly
* Hash passwords directly
* Validate credentials manually

All must be inside service.

---

## 5.1 Required Service Methods

```python
authenticate_user(email, password)
register_student(form_data)
register_company(form_data)
logout_current_user()
hash_password(password)
verify_password(password, password_hash)
```

---

# 6️⃣ LOGIN CONTRACT

## 6.1 Login Form Fields (Template)

Must use:

```html
name="email"
name="password"
```

Never:

* `username`
* `user_email`
* `pass`

---

## 6.2 Login Service Return Contract

`authenticate_user()` must return:

```python
{
    "user": User | None,
    "error": str | None
}
```

Never return vague:

```
result
data
response
```

---

## 6.3 Login Redirect Rules

After login:

| Role    | Redirect To          |
| ------- | -------------------- |
| admin   | `/admin/dashboard`   |
| company | `/company/dashboard` |
| student | `/student/dashboard` |

This mapping must exist in auth route, not in template.

---

# 7️⃣ REGISTRATION CONTRACT

---

## 7.1 Student Registration Contract

Route:

```python
register_student_view()
```

Service:

```python
register_student(form_data)
```

Required form keys:

```python
{
    "email": str,
    "password": str,
    "student_id": str,
    "name": str,
    "branch": str,
    "cgpa": float
}
```

Role automatically set to:

```python
role = STUDENT
```

---

## 7.2 Company Registration Contract

Route:

```python
register_company_view()
```

Service:

```python
register_company(form_data)
```

Required form keys:

```python
{
    "email": str,
    "password": str,
    "company_name": str,
    "hr_email": str,
    "website": str
}
```

Role automatically set to:

```python
role = COMPANY
```

Approval status must default to:

```python
approval_status = "pending"
```

Company must NOT be auto-approved.

---

# 8️⃣ PASSWORD HANDLING RULES

Never store:

```
password
```

Only:

```
password_hash
```

Hashing must be done inside:

```python
hash_password(password)
```

Verification must use:

```python
verify_password(password, password_hash)
```

Routes must never compare plaintext passwords.

---

# 9️⃣ SESSION & LOGIN RULES

Using Flask-Login:

User model must implement:

```python
get_id()
is_authenticated
is_active
```

`is_active` must reflect:

* user.is_active
* NOT blacklisted status (blacklist handled elsewhere)

---

# 🔟 ACCOUNT STATUS RULES

Auth must block login if:

```
user.is_active == False
```

For company:

Also block if:

```
approval_status != "approved"
```

This check must happen inside `authenticate_user()`.

Never check approval inside template.

---

# 1️⃣1️⃣ TEMPLATE CONTRACT

Templates must live in:

```
templates/auth/
```

Required files:

```
login.html
register_student.html
register_company.html
```

---

## Template Variable Contract

Login page must accept:

```python
{
    "error": str | None
}
```

Registration pages must accept:

```python
{
    "error": str | None
}
```

Never:

```
message
msg
response
```

Standardize to `error`.

---

# 1️⃣2️⃣ ERROR HANDLING RULE

Auth service must return clear messages:

Examples:

```
"Invalid credentials"
"Account not approved yet"
"Account is deactivated"
"Email already registered"
```

Never expose:

* raw DB errors
* tracebacks
* internal exceptions

---

# 1️⃣3️⃣ FORBIDDEN PRACTICES

❌ Role-based redirect inside template
❌ Password comparison inside route
❌ Setting role manually from form
❌ Hardcoded role strings
❌ Allowing admin registration via UI
❌ Login route querying company table directly

Auth only touches:

```
users
students (during registration)
companies (during registration)
```

---

# 1️⃣4️⃣ AUTH FLOW GUARANTEE

Correct flow:

```
Route (auth/routes.py)
    ↓
auth_service
    ↓
User model
    ↓
Return contract dict
    ↓
Route handles redirect
```

Templates never decide behavior.

---

# 🧠 What This Prevents

* Broken role redirects
* Login bypasses
* Company login before approval
* Plaintext password mistakes
* Registration inconsistency
* Security leaks

---


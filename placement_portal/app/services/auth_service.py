"""
AuthService -> This is done here by werkzeug (a flask module)
===========
#RBAC - authentication and authorization according to the user role types
Domain: Identity & Authentication

Purpose:
--------
Responsible for all identity-related operations including:
- User registration (student & company)
- Credential validation
- Password hashing & verification
- Login authentication
- Role assignment enforcement

Business Responsibility:
------------------------
Determines *who* a user is and whether they are allowed to access the system.

Does NOT Handle:
----------------
- Drive creation
- Application lifecycle
- Approval workflows
- Business domain transitions

Reason To Change:
-----------------
Changes in authentication policy such as:
- Password strength rules
- Email verification logic
- OAuth/JWT implementation
- Multi-factor authentication
"""


"""
AuthService
===========

Domain: Identity & Authentication

Responsibilities:
- Secure registration (student & company)
- Credential validation
- Password hashing & verification
- Role-based login control
- Governance enforcement
"""

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User
from app.models.student import Student
from app.models.company import Company
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_required,
    validate_cgpa,
)
from app.utils.constants import (
    STUDENT,
    COMPANY,
    ADMIN,
    COMPANY_APPROVED,
)


class AuthService:

    # ----------------------------------------------------------
    # PASSWORD HELPERS
    # ----------------------------------------------------------

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, password_hash):
        return check_password_hash(password_hash, password)

    # ----------------------------------------------------------
    # STUDENT REGISTRATION
    # ----------------------------------------------------------

    @staticmethod
    def register_student(form_data):

        email = (form_data.get("email") or "").strip().lower()
        password = form_data.get("password")
        name = form_data.get("name")
        student_id = (form_data.get("student_id") or "").strip()
        branch = form_data.get("branch")
        cgpa = form_data.get("cgpa")

        # ---- Validation ----

        email_error = validate_email(email)
        if email_error:
            return {"user": None, "error": email_error}

        password_error = validate_password(password)
        if password_error:
            return {"user": None, "error": password_error}

        name_error = validate_required(name, "Name")
        if name_error:
            return {"user": None, "error": name_error}

        student_id_error = validate_required(student_id, "Student ID")
        if student_id_error:
            return {"user": None, "error": student_id_error}

        branch_error = validate_required(branch, "Branch")
        if branch_error:
            return {"user": None, "error": branch_error}

        cgpa_error = validate_cgpa(cgpa)
        if cgpa_error:
            return {"user": None, "error": cgpa_error}

        cgpa = float(cgpa)

        # ---- Duplicate Checks ----

        if User.query.filter_by(email=email).first():
            return {"user": None, "error": "Email already registered"}

        if Student.query.filter_by(student_id=student_id).first():
            return {"user": None, "error": "Student ID already registered"}

        try:
            # ---- Create User ----
            user = User(
                email=email,
                password_hash=AuthService.hash_password(password),
                role=STUDENT,
            )

            db.session.add(user)
            db.session.flush()

            # ---- Create Student Profile ----
            student = Student(
                user_id=user.id,
                student_id=student_id,
                name=name.strip(),
                branch=branch.strip(),
                cgpa=cgpa,
            )

            db.session.add(student)
            db.session.commit()

            return {"user": user, "error": None}

        except IntegrityError:
            db.session.rollback()
            return {"user": None, "error": "Registration failed"}

    # ----------------------------------------------------------
    # COMPANY REGISTRATION
    # ----------------------------------------------------------

    @staticmethod
    def register_company(form_data):

        email = (form_data.get("email") or "").strip().lower()
        password = form_data.get("password")
        company_name = form_data.get("company_name")
        hr_email = (form_data.get("hr_email") or "").strip().lower()
        website = (form_data.get("website") or "").strip()

        # ---- Validation ----

        email_error = validate_email(email)
        if email_error:
            return {"user": None, "error": email_error}

        password_error = validate_password(password)
        if password_error:
            return {"user": None, "error": password_error}

        name_error = validate_required(company_name, "Company Name")
        if name_error:
            return {"user": None, "error": name_error}

        hr_error = validate_email(hr_email)
        if hr_error:
            return {"user": None, "error": "Invalid HR email"}

        if User.query.filter_by(email=email).first():
            return {"user": None, "error": "Email already registered"}

        try:
            # ---- Create User ----
            user = User(
                email=email,
                password_hash=AuthService.hash_password(password),
                role=COMPANY,
            )

            db.session.add(user)
            db.session.flush()

            # ---- Create Company Profile ----
            company = Company(
                user_id=user.id,
                company_name=company_name.strip(),
                hr_email=hr_email,
                website=website or None,
            )

            db.session.add(company)
            db.session.commit()

            return {"user": user, "error": None}

        except IntegrityError:
            db.session.rollback()
            return {"user": None, "error": "Registration failed"}

    # ----------------------------------------------------------
    # AUTHENTICATION
    # ----------------------------------------------------------

    @staticmethod
    def authenticate_user(email, password):

        email = (email or "").strip().lower()

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"user": None, "error": "Invalid credentials"}

        if not AuthService.verify_password(password, user.password_hash):
            return {"user": None, "error": "Invalid credentials"}

        if not user.is_active:
            return {"user": None, "error": "Account is deactivated"}

        # ---- Role Guard ----
        if user.role not in (STUDENT, COMPANY, ADMIN):
            return {"user": None, "error": "Invalid role configuration"}

        # ---- STUDENT GOVERNANCE ----
        if user.role == STUDENT:
            student = getattr(user, "student", None)
            if not student:
                return {"user": None, "error": "Student profile missing"}
            if student.is_blacklisted:
                return {"user": None, "error": "Account is blacklisted"}

        # ---- COMPANY GOVERNANCE ----
        if user.role == COMPANY:
            company = getattr(user, "company", None)
            if not company:
                return {"user": None, "error": "Company profile missing"}
            if company.approval_status != COMPANY_APPROVED:
                return {"user": None, "error": "Company not approved yet"}
            if company.is_blacklisted:
                return {"user": None, "error": "Company account is blacklisted"}

        return {"user": user, "error": None}
from functools import wraps
from flask_login import current_user
from flask import abort

from app.utils.constants import (
    ADMIN,
    COMPANY,
    STUDENT,
    COMPANY_APPROVED,
)


# ----------------------------------------------------------
# ADMIN REQUIRED
# ----------------------------------------------------------

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != ADMIN:
            abort(403)

        if not current_user.is_active:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


# ----------------------------------------------------------
# COMPANY REQUIRED
# ----------------------------------------------------------

def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != COMPANY:
            abort(403)

        if not current_user.is_active:
            abort(403)

        company = getattr(current_user, "company", None)

        if not company:
            abort(403)

        if company.approval_status != COMPANY_APPROVED:
            abort(403)

        if company.is_blacklisted:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function


# ----------------------------------------------------------
# STUDENT REQUIRED
# ----------------------------------------------------------

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(401)

        if current_user.role != STUDENT:
            abort(403)

        if not current_user.is_active:
            abort(403)

        student = getattr(current_user, "student", None)

        if not student:
            abort(403)

        if student.is_blacklisted:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function
import re


# ----------------------------------------------------------
# EMAIL VALIDATION
# ----------------------------------------------------------

def validate_email(email):
    if email is None:
        return "Email is required"

    email = email.strip().lower()

    if not email:
        return "Email is required"

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return "Invalid email format"

    return None


# ----------------------------------------------------------
# PASSWORD VALIDATION
# ----------------------------------------------------------

def validate_password(password):
    if password is None:
        return "Password is required"

    password = password.strip()

    if len(password) < 8:
        return "Password must be at least 8 characters"

    return None


# ----------------------------------------------------------
# REQUIRED FIELD VALIDATION
# ----------------------------------------------------------

def validate_required(field_value, field_name):

    if field_value is None:
        return f"{field_name} is required"

    if isinstance(field_value, str) and not field_value.strip():
        return f"{field_name} is required"

    return None


# ----------------------------------------------------------
# CGPA VALIDATION
# ----------------------------------------------------------

def validate_cgpa(cgpa):

    if cgpa is None:
        return "CGPA is required"

    if isinstance(cgpa, str):
        cgpa = cgpa.strip()

    try:
        cgpa = float(cgpa)
    except (TypeError, ValueError):
        return "Invalid CGPA"

    if not 0 <= cgpa <= 10:
        return "CGPA must be between 0 and 10"

    return None
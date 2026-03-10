# ==========================================================
# ROLES
# ==========================================================

ADMIN = "admin"
STUDENT = "student"
COMPANY = "company"


# ==========================================================
# COMPANY APPROVAL STATUS
# ==========================================================

COMPANY_PENDING = "pending"
COMPANY_APPROVED = "approved"
COMPANY_REJECTED = "rejected"


# ==========================================================
# DRIVE STATUS
# ==========================================================

DRIVE_PENDING = "pending"
DRIVE_APPROVED = "approved"
DRIVE_REJECTED = "rejected"
DRIVE_CLOSED = "closed"


# ==========================================================
# APPLICATION STATUS
# ==========================================================

APPLICATION_APPLIED = "applied"
APPLICATION_SHORTLISTED = "shortlisted"
APPLICATION_SELECTED = "selected"
APPLICATION_REJECTED = "rejected"


# ==========================================================
# DRIVE STATE MACHINE
# ==========================================================

DRIVE_ALLOWED_TRANSITIONS = {
    DRIVE_PENDING: {DRIVE_APPROVED, DRIVE_REJECTED},
    DRIVE_APPROVED: {DRIVE_CLOSED},
    DRIVE_REJECTED: set(),
    DRIVE_CLOSED: set(),
}


# ==========================================================
# APPLICATION STATE MACHINE
# ==========================================================

APPLICATION_ALLOWED_TRANSITIONS = {
    APPLICATION_APPLIED: {
        APPLICATION_SHORTLISTED,
        APPLICATION_REJECTED,
    },
    APPLICATION_SHORTLISTED: {
        APPLICATION_SELECTED,
        APPLICATION_REJECTED,
    },
    APPLICATION_SELECTED: set(),
    APPLICATION_REJECTED: set(),
}
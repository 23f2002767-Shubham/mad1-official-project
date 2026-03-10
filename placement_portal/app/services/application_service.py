"""
ApplicationService
==================

Domain: Student-Drive Interaction (Relationship Management)

Responsibilities:
- Apply to drive
- Prevent duplicate applications
- Enforce eligibility & governance rules
- Manage controlled status transitions (state machine)
- Fetch student & drive application data

Owns:
- The lifecycle of student participation in placement drives.
"""

from datetime import date
from sqlalchemy import or_

from app.extensions import db
from app.models.application import Application
from app.models.placement_drive import PlacementDrive
from app.models.student import Student
from app.utils.constants import (
    APPLICATION_APPLIED,
    APPLICATION_SHORTLISTED,
    APPLICATION_SELECTED,
    APPLICATION_REJECTED,
    APPLICATION_ALLOWED_TRANSITIONS,
    DRIVE_APPROVED,
)


class ApplicationService:

    # ==========================================================
    # INTERNAL RESULT HELPERS (UNIFIED RETURN CONTRACT)
    # ==========================================================

    @staticmethod
    def _success(message, data=None):
        return {
            "success": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def _failure(message):
        return {
            "success": False,
            "message": message,
            "data": None,
        }

    # ==========================================================
    # APPLY TO DRIVE (STUDENT)
    # ==========================================================

    @staticmethod
    def apply_to_drive(student_id, drive_id):

        student = Student.query.get(student_id)
        if not student:
            return ApplicationService._failure("Student not found")

        # 🔒 Governance: Blacklisted students cannot apply
        if student.is_blacklisted:
            return ApplicationService._failure(
                "Student account is blacklisted"
            )

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return ApplicationService._failure("Drive not found")

        # Only approved drives are visible/applicable
        if drive.status != DRIVE_APPROVED:
            return ApplicationService._failure(
                "Drive is not available for application"
            )

        # Deadline enforcement
        if drive.application_deadline < date.today():
            return ApplicationService._failure(
                "Application deadline has passed"
            )

        # Duplicate prevention
        existing = Application.query.filter_by(
            student_id=student_id,
            drive_id=drive_id
        ).first()

        if existing:
            return ApplicationService._failure(
                "Already applied to this drive"
            )

        application = Application(
            student_id=student_id,
            drive_id=drive_id,
            status=APPLICATION_APPLIED,
        )

        db.session.add(application)
        db.session.commit()

        return ApplicationService._success(
            "Application submitted successfully",
            application
        )

    # ==========================================================
    # INTERNAL STATE MACHINE TRANSITION
    # ==========================================================

    @staticmethod
    def _transition(application, new_status):

        allowed = APPLICATION_ALLOWED_TRANSITIONS.get(
            application.status,
            set()
        )

        if new_status not in allowed:
            return ApplicationService._failure(
                "Invalid application state transition"
            )

        application.status = new_status
        db.session.commit()

        return ApplicationService._success(
            "Application status updated successfully"
        )

    # ==========================================================
    # COMPANY STATUS TRANSITIONS
    # ==========================================================

    @staticmethod
    def shortlist_application(application_id):

        application = Application.query.get(application_id)
        if not application:
            return ApplicationService._failure("Application not found")

        return ApplicationService._transition(
            application,
            APPLICATION_SHORTLISTED
        )

    @staticmethod
    def select_application(application_id):

        application = Application.query.get(application_id)
        if not application:
            return ApplicationService._failure("Application not found")

        return ApplicationService._transition(
            application,
            APPLICATION_SELECTED
        )

    @staticmethod
    def reject_application(application_id):

        application = Application.query.get(application_id)
        if not application:
            return ApplicationService._failure("Application not found")

        return ApplicationService._transition(
            application,
            APPLICATION_REJECTED
        )

    # ==========================================================
    # FETCH METHODS (READ-ONLY)
    # ==========================================================

    @staticmethod
    def get_student_applications(student_id):
        return (
            Application.query
            .filter_by(student_id=student_id)
            .order_by(Application.id.desc())
            .all()
        )

    @staticmethod
    def get_drive_applications(drive_id):
        return (
            Application.query
            .filter_by(drive_id=drive_id)
            .order_by(Application.id.desc())
            .all()
        )

    @staticmethod
    def get_student_placement_history(student_id):
        return (
            Application.query
            .filter_by(
                student_id=student_id,
                status=APPLICATION_SELECTED
            )
            .order_by(Application.id.desc())
            .all()
        )
   
    # ----------------------------------------------------------
    # GET APPLICATION BY ID
    # ----------------------------------------------------------

    @staticmethod
    def get_application_by_id(application_id):

        application = Application.query.get(application_id)

        if not application:
            return ApplicationService._failure("Application not found")

        return ApplicationService._success(
            "Application fetched successfully",
            application
        )

    # ==========================================================
    # ADMIN-LEVEL FETCH (OPTIONAL EXTENSION)
    # ==========================================================

    @staticmethod
    def get_all_applications(q=None, page=1, per_page=10):

        query = Application.query

        if q:
            query = query.join(Student).filter(
                or_(
                    Student.name.ilike(f"%{q}%"),
                    Student.student_id.ilike(f"%{q}%")
                )
            )

        pagination = query.order_by(
            Application.id.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return pagination.items, pagination
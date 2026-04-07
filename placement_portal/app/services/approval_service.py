'''
Company must be approved by admin only then it can login and create drives
'''

from app.extensions import db
from app.models.company import Company
from app.models.placement_drive import PlacementDrive
from app.models.student import Student
from app.models.application import Application
from app.utils.constants import (
    COMPANY_PENDING,
    COMPANY_APPROVED,
    COMPANY_REJECTED,
    DRIVE_PENDING,
    DRIVE_APPROVED,
    DRIVE_REJECTED,
    DRIVE_CLOSED,
    DRIVE_ALLOWED_TRANSITIONS,
)

from sqlalchemy import or_


class ApprovalService:

    # ==========================================================
    # INTERNAL HELPERS
    # ==========================================================

    @staticmethod
    def _paginate(query, page, per_page=10):
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination

    @staticmethod
    def _success(message):
        return {"success": True, "message": message}

    @staticmethod
    def _failure(message):
        return {"success": False, "message": message}

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    @staticmethod
    def get_admin_dashboard_stats():
        return {
            "total_students": Student.query.count(),
            "total_companies": Company.query.count(),
            "total_drives": PlacementDrive.query.count(),
            "total_applications": Application.query.count(),
        }

    # ==========================================================
    # LISTING WITH SEARCH + PAGINATION
    # ==========================================================

    @staticmethod
    def get_pending_companies(q, page):
        query = Company.query.filter_by(approval_status=COMPANY_PENDING)

        if q:
            query = query.filter(
                or_(
                    Company.company_name.ilike(f"%{q}%"),
                    Company.hr_email.ilike(f"%{q}%"),
                )
            )

        query = query.order_by(Company.id.desc())
        return ApprovalService._paginate(query, page)

    @staticmethod
    def get_pending_drives(q, page):
        query = PlacementDrive.query.filter_by(status=DRIVE_PENDING)

        if q:
            query = query.filter(
                PlacementDrive.job_title.ilike(f"%{q}%")
            )

        query = query.order_by(PlacementDrive.id.desc())
        return ApprovalService._paginate(query, page)

    @staticmethod
    def get_all_students(q, page):
        query = Student.query

        if q:
            query = query.filter(
                or_(
                    Student.name.ilike(f"%{q}%"),
                    Student.student_id.ilike(f"%{q}%"),
                )
            )

        query = query.order_by(Student.id.desc())
        return ApprovalService._paginate(query, page)

    @staticmethod
    def get_all_companies(q, page):
        query = Company.query

        if q:
            query = query.filter(
                or_(
                    Company.company_name.ilike(f"%{q}%"),
                    Company.hr_email.ilike(f"%{q}%"),
                )
            )

        query = query.order_by(Company.id.desc())
        return ApprovalService._paginate(query, page)

    @staticmethod
    def get_all_applications(q, page):
        query = Application.query

        if q:
            query = query.join(Student).filter(
                Student.name.ilike(f"%{q}%")
            )

        query = query.order_by(Application.id.desc())
        return ApprovalService._paginate(query, page)

    # ==========================================================
    # COMPANY APPROVAL
    # ==========================================================

    @staticmethod
    def approve_company(company_id):
        company = Company.query.get(company_id)

        if not company:
            return ApprovalService._failure("Company not found")

        if company.approval_status != COMPANY_PENDING:
            return ApprovalService._failure("Invalid approval state")

        company.approval_status = COMPANY_APPROVED
        db.session.commit()

        return ApprovalService._success("Company approved successfully.")

    @staticmethod
    def reject_company(company_id):
        company = Company.query.get(company_id)

        if not company:
            return ApprovalService._failure("Company not found")

        if company.approval_status != COMPANY_PENDING:
            return ApprovalService._failure("Invalid rejection state")

        company.approval_status = COMPANY_REJECTED
        db.session.commit()

        return ApprovalService._success("Company rejected successfully.")

    # ==========================================================
    # DRIVE TRANSITION ENGINE
    # ==========================================================

    @staticmethod
    def _transition_drive(drive, new_status):

        allowed = DRIVE_ALLOWED_TRANSITIONS.get(drive.status, set())

        if new_status not in allowed:
            return ApprovalService._failure("Invalid drive state transition")

        drive.status = new_status
        return ApprovalService._success("Drive status updated")

    # ==========================================================
    # DRIVE APPROVAL
    # ==========================================================

    @staticmethod
    def approve_drive(drive_id):
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return ApprovalService._failure("Drive not found")

        result = ApprovalService._transition_drive(drive, DRIVE_APPROVED)

        if not result["success"]:
            return result

        db.session.commit()
        return ApprovalService._success("Placement drive approved successfully.")

    @staticmethod
    def reject_drive(drive_id):
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return ApprovalService._failure("Drive not found")

        result = ApprovalService._transition_drive(drive, DRIVE_REJECTED)

        if not result["success"]:
            return result

        db.session.commit()
        return ApprovalService._success("Placement drive rejected successfully.")

    # ==========================================================
    # STUDENT BLACKLIST
    # ==========================================================

    @staticmethod
    def blacklist_student(student_id):
        student = Student.query.get(student_id)

        if not student:
            return ApprovalService._failure("Student not found")

        if student.is_blacklisted:
            return ApprovalService._failure("Student already blacklisted")

        student.is_blacklisted = True
        db.session.commit()

        return ApprovalService._success("Student blacklisted successfully.")

    @staticmethod
    def activate_student(student_id):
        student = Student.query.get(student_id)

        if not student:
            return ApprovalService._failure("Student not found")

        if not student.is_blacklisted:
            return ApprovalService._failure("Student is not blacklisted")

        student.is_blacklisted = False
        db.session.commit()

        return ApprovalService._success("Student reactivated successfully.")

    # ==========================================================
    # COMPANY BLACKLIST
    # ==========================================================

    @staticmethod
    def blacklist_company(company_id):
        company = Company.query.get(company_id)

        if not company:
            return ApprovalService._failure("Company not found")

        if company.is_blacklisted:
            return ApprovalService._failure("Company already blacklisted")

        company.is_blacklisted = True

        # Close approved drives safely
        for drive in company.drives:
            if drive.status == DRIVE_APPROVED:
                ApprovalService._transition_drive(drive, DRIVE_CLOSED)

        db.session.commit()
        return ApprovalService._success("Company blacklisted successfully.")

    @staticmethod
    def activate_company(company_id):
        company = Company.query.get(company_id)

        if not company:
            return ApprovalService._failure("Company not found")

        if not company.is_blacklisted:
            return ApprovalService._failure("Company is not blacklisted")

        company.is_blacklisted = False
        db.session.commit()

        return ApprovalService._success("Company reactivated successfully.")

    # ==========================================================
    # REPORTS
    # ==========================================================

    @staticmethod
    def get_reports_stats():
        total_selected = Application.query.filter_by(status="APPLICATION_SELECTED").count()
        total_rejected = Application.query.filter_by(status="APPLICATION_REJECTED").count()

        total = total_selected + total_rejected
        selection_ratio = round((total_selected / total) * 100, 2) if total else 0

        return {
            "total_selected": total_selected,
            "total_rejected": total_rejected,
            "selection_ratio": selection_ratio,
        }
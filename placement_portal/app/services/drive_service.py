"""
DriveService
============

Domain: Opportunity Management

Purpose:
--------
Manages placement drive (job posting) lifecycle including:
- Drive creation by companies
- Fetching company drives
- Fetching approved drives for students
- Retrieving specific drive details

Business Responsibility:
------------------------
Owns the lifecycle and structure of job opportunities within the system.

Does NOT Handle:
----------------
- Student applications
- Application status transitions
- Authentication logic
- Admin governance decisions

Reason To Change:
-----------------
Changes in drive-related policies such as:
- Eligibility validation rules
- Deadline enforcement logic
- Drive editing rules
- Drive visibility rules
"""

"""
DriveService
============

Domain: Opportunity Management

Responsibilities:
- Drive creation
- Drive lifecycle control (state-machine enforced)
- Drive closing
- Visibility enforcement
- Ownership validation
"""

from datetime import datetime, date
from app.extensions import db
from app.models.company import Company
from app.models.placement_drive import PlacementDrive
from app.utils.constants import (
    COMPANY_APPROVED,
    DRIVE_PENDING,
    DRIVE_APPROVED,
    DRIVE_CLOSED,
    DRIVE_ALLOWED_TRANSITIONS,
)


class DriveService:

    # ----------------------------------------------------------
    # CREATE DRIVE
    # ----------------------------------------------------------

    @staticmethod
    def create_drive(company_id, form_data):

        company = Company.query.get(company_id)
        if not company:
            return {"error": "Company not found"}

        if company.approval_status != COMPANY_APPROVED:
            return {"error": "Company not approved"}

        if company.is_blacklisted:
            return {"error": "Company is blacklisted"}

        job_title = (form_data.get("job_title") or "").strip()
        job_description = (form_data.get("job_description") or "").strip()
        eligibility_criteria = (form_data.get("eligibility_criteria") or "").strip()
        deadline_str = form_data.get("application_deadline")

        if not job_title:
            return {"error": "Job title is required"}

        if not job_description:
            return {"error": "Job description is required"}

        if not eligibility_criteria:
            return {"error": "Eligibility criteria required"}

        if not deadline_str:
            return {"error": "Application deadline required"}

        try:
            deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid deadline format"}

        if deadline_date <= date.today():
            return {"error": "Deadline must be in the future"}

        drive = PlacementDrive(
            company_id=company.id,
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility_criteria,
            application_deadline=deadline_date,
            status=DRIVE_PENDING,
        )

        db.session.add(drive)
        db.session.commit()

        return {"drive": drive, "error": None}

    # ----------------------------------------------------------
    # INTERNAL TRANSITION ENGINE
    # ----------------------------------------------------------

    @staticmethod
    def _transition(drive, new_status):

        allowed = DRIVE_ALLOWED_TRANSITIONS.get(
            drive.status,
            set()
        )

        if new_status not in allowed:
            return {"error": "Invalid drive state transition"}

        drive.status = new_status
        db.session.commit()

        return {"error": None}

    # ----------------------------------------------------------
    # CLOSE DRIVE (Company)
    # ----------------------------------------------------------

    @staticmethod
    def close_drive(drive_id, company_id):

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"error": "Drive not found"}

        if drive.company_id != company_id:
            return {"error": "Unauthorized access"}

        return DriveService._transition(drive, DRIVE_CLOSED)

    # ----------------------------------------------------------
    # GET COMPANY DRIVES
    # ----------------------------------------------------------

    @staticmethod
    def get_company_drives(company_id):

        return PlacementDrive.query.filter_by(
            company_id=company_id
        ).order_by(
            PlacementDrive.id.desc()
        ).all()

    # ----------------------------------------------------------
    # GET DRIVE BY ID
    # ----------------------------------------------------------

    @staticmethod
    def get_drive_by_id(drive_id):
        return PlacementDrive.query.get(drive_id)

    # ----------------------------------------------------------
    # GET APPROVED DRIVES (VISIBLE TO STUDENTS)
    # ----------------------------------------------------------

    @staticmethod
    def get_approved_drives():

        return PlacementDrive.query.filter(
            PlacementDrive.status == DRIVE_APPROVED,
            PlacementDrive.application_deadline >= date.today()
        ).order_by(
            PlacementDrive.application_deadline.asc()
        ).all()
    

# ----------------------------------------------------------
# UPDATE DRIVE (Company)
# ----------------------------------------------------------

    @staticmethod
    def update_drive(drive_id, form_data):


        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"error": "Drive not found"}
        
        # 🚨 Prevent editing closed drives
        if drive.status == "closed":
            return {"error": "Closed drives cannot be edited"}

        drive.job_title = (form_data.get("job_title") or "").strip()
        drive.job_description = (form_data.get("job_description") or "").strip()
        drive.eligibility_criteria = (form_data.get("eligibility_criteria") or "").strip()
        
        deadline_str = form_data.get("application_deadline")
        if deadline_str:
            try:
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                #validation to ensure deadline is in the future
                if deadline_date <= date.today():
                    return {"error": "Deadline must be in the future"}
                drive.application_deadline = deadline_date
            except ValueError:
                return {"error": "Invalid deadline format"}


        db.session.commit()

        return {"error": None}






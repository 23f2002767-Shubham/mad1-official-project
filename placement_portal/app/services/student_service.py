"""
StudentService
==============

Domain: Student Management

Responsibilities:
- Student dashboard aggregation
- Fetch available drives for students
- Update student profile
- Handle resume upload
"""

from datetime import date
from werkzeug.utils import secure_filename
import os

from app.extensions import db
from app.models.student import Student
from app.models.placement_drive import PlacementDrive
from app.services.application_service import ApplicationService
from app.utils.constants import DRIVE_APPROVED , APPLICATION_SELECTED
from flask import current_app


class StudentService:

    # ----------------------------------------------------------
    # DASHBOARD DATA
    # ----------------------------------------------------------

    @staticmethod
    def get_student_dashboard_data(student_id):

        student = Student.query.get(student_id)

        if not student:
            return None

        # Fetch drives
        approved_drives = (
            PlacementDrive.query.filter(
                PlacementDrive.status == DRIVE_APPROVED,
                PlacementDrive.application_deadline >= date.today()
            )
            .order_by(PlacementDrive.application_deadline.asc())
            .all()
        )

        # Fetch applications
        applications = ApplicationService.get_student_applications(student_id)

        applied_drive_ids = {app.drive_id for app in applications}

        selected_count = sum(
            1 for app in applications if app.status == APPLICATION_SELECTED
        )

        return {
            "student": student,
            "approved_drives": approved_drives,
            "available_drives_count": len(approved_drives),
            "applied_drives_count": len(applications),
            "selected_count": selected_count,
            "recent_applications": applications[:5],
            "applied_drive_ids": applied_drive_ids,
        }

    # ----------------------------------------------------------
    # AVAILABLE DRIVES
    # ----------------------------------------------------------

    @staticmethod
    def get_available_drives(student_id):

        student = Student.query.get(student_id)

        if not student:
            return []

        drives = (
            PlacementDrive.query.filter(
                PlacementDrive.status == DRIVE_APPROVED,
                PlacementDrive.application_deadline >= date.today()
            )
            .order_by(PlacementDrive.application_deadline.asc())
            .all()
        )

        return drives

    # ----------------------------------------------------------
    # UPDATE STUDENT PROFILE
    # ----------------------------------------------------------

    @staticmethod
    def update_student_profile(student_id, form_data):

        student = Student.query.get(student_id)

        if not student:
            return {"error": "Student not found"}

        student.name = (form_data.get("name") or "").strip()
        student.branch = (form_data.get("branch") or "").strip()

        cgpa = form_data.get("cgpa")

        if cgpa:
            try:
                student.cgpa = float(cgpa)
            except ValueError:
                return {"error": "Invalid CGPA"}

        db.session.commit()

        return {"error": None}

    # ----------------------------------------------------------
    # UPLOAD RESUME
    # ----------------------------------------------------------

    @staticmethod
    def upload_resume(student_id, file):

        student = Student.query.get(student_id)

        if not student:
            return {"error": "Student not found"}

        if not file:
            return {"error": "No file uploaded"}

        filename = secure_filename(file.filename)

        if not filename:
            return {"error": "Invalid file"}

        # Allowed formats
        allowed_extensions = {"pdf", "doc", "docx"}

        ext = filename.rsplit(".", 1)[-1].lower()

        if ext not in allowed_extensions:
            return {"error": "Invalid file type"}

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        new_filename = f"{student.student_id}_resume.{ext}"

        file_path = os.path.join(upload_folder, new_filename)

        file.save(file_path)

        student.resume_path = f"uploads/resumes/{new_filename}"
        student.is_resume_uploaded = True

        db.session.commit()

        return {"error": None}
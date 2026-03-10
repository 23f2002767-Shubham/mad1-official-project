from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from flask_login import login_required, current_user

from app.decorators import company_required
from app.services.drive_service import DriveService
from app.services.application_service import ApplicationService
from app.extensions import db

# 🔐 IMPORT CONSTANTS (NO HARDCODED STRINGS)
from app.utils.constants import (
    DRIVE_CLOSED,
    APPLICATION_SHORTLISTED,
)

company_bp = Blueprint("company", __name__, url_prefix="/company")


# ==========================================================
# DASHBOARD
# ==========================================================

@company_bp.route("/dashboard")
@login_required
@company_required
def company_dashboard_view():

    company = current_user.company
    drives = DriveService.get_company_drives(company.id)

    total_drives = len(drives)

    open_drives = len(
        [drive for drive in drives if drive.status != DRIVE_CLOSED]
    )

    closed_drives = len(
        [drive for drive in drives if drive.status == DRIVE_CLOSED]
    )

    total_applications = 0
    for drive in drives:
        if hasattr(drive, "applications"):
            total_applications += len(drive.applications)

    return render_template(
        "company/dashboard.html",
        drives=drives,
        total_drives=total_drives,
        open_drives=open_drives,
        closed_drives=closed_drives,
        total_applications=total_applications,
    )


# ==========================================================
# CREATE DRIVE
# ==========================================================

@company_bp.route("/create-drive", methods=["GET", "POST"])
@login_required
@company_required
def create_drive_view():

    company = current_user.company

    if request.method == "POST":

        result = DriveService.create_drive(company.id, request.form)

        if result.get("error"):
            flash(result["error"], "danger")
            return redirect(url_for("company.create_drive_view"))

        flash(
            "Placement drive created successfully (Pending Admin Approval).",
            "success",
        )
        return redirect(url_for("company.company_dashboard_view"))

    return render_template("company/create_drive.html")

# ==========================================================
# MY DRIVES
# ==========================================================

@company_bp.route("/my-drives")
@login_required
@company_required
def my_drives_view():

    company = current_user.company
    drives = DriveService.get_company_drives(company.id)

    return render_template(
        "company/my_drives.html",
        drives=drives,
    )

# ==========================================================
# DRIVE DETAIL
# ==========================================================

@company_bp.route("/drive/<int:drive_id>")
@login_required
@company_required
def drive_detail_view(drive_id):

    drive = DriveService.get_drive_by_id(drive_id)

    if not drive:
        abort(404)

    if drive.company_id != current_user.company.id:
        abort(403)

    applications = ApplicationService.get_drive_applications(drive_id)

    return render_template(
        "company/drive_detail.html",
        drive=drive,
        applications_count=len(applications),
    )


# ==========================================================
# EDIT DRIVE
# ==========================================================

@company_bp.route("/drive/<int:drive_id>/edit", methods=["GET", "POST"])
@login_required
@company_required
def edit_drive_view(drive_id):

    drive = DriveService.get_drive_by_id(drive_id)

    if not drive:
        abort(404)

    if drive.company_id != current_user.company.id:
        abort(403)

    if request.method == "POST":

        result = DriveService.update_drive(drive_id, request.form)

        if result.get("error"):
            flash(result["error"], "danger")
        else:
            flash("Drive updated successfully", "success")

        return redirect(url_for("company.drive_detail_view", drive_id=drive_id))

    return render_template(
        "company/edit_drive.html",
        drive=drive
    )



# ==========================================================
# CLOSE DRIVE
# ==========================================================

@company_bp.route("/close-drive/<int:drive_id>", methods=["POST"])
@login_required
@company_required
def close_drive_view(drive_id):

    company = current_user.company
    result = DriveService.close_drive(drive_id, company.id)

    if result.get("error"):
        flash(result["error"], "danger")
    else:
        flash("Drive closed successfully.", "warning")

    return redirect(url_for("company.company_dashboard_view"))


# ==========================================================
# VIEW APPLICANTS
# ==========================================================

@company_bp.route("/drive/<int:drive_id>/applicants")
@login_required
@company_required
def view_applicants_view(drive_id):

    drive = DriveService.get_drive_by_id(drive_id)

    if not drive:
        abort(404)

    if drive.company_id != current_user.company.id:
        abort(403)

    applications = ApplicationService.get_drive_applications(drive_id)

    return render_template(
        "company/applications.html",
        drive=drive,
        applications=applications,
    )


# ==========================================================
# SHORTLISTED CANDIDATES
# ==========================================================

@company_bp.route("/drive/<int:drive_id>/shortlisted")
@login_required
@company_required
def shortlisted_candidates_view(drive_id):

    drive = DriveService.get_drive_by_id(drive_id)

    if not drive:
        abort(404)

    if drive.company_id != current_user.company.id:
        abort(403)

    applications = ApplicationService.get_drive_applications(drive_id)

    shortlisted_applications = [
        app
        for app in applications
        if app.status == APPLICATION_SHORTLISTED
    ]

    return render_template(
        "company/shortlisted_candidates.html",
        drive=drive,
        shortlisted_applications=shortlisted_applications,
    )

"""
# ==========================================================
# SHORTLIST
# ==========================================================

@company_bp.route("/application/<int:application_id>/shortlist", methods=["POST"])
@login_required
@company_required
def shortlist_application_view(application_id):

    application = ApplicationService.get_application_by_id(application_id)

    if not application:
        abort(404)

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.shortlist_application(application_id)

    if result.get("error"):
        flash(result["error"], "danger")
    else:
        flash("Candidate shortlisted successfully.", "success")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )


# ==========================================================
# SELECT
# ==========================================================

@company_bp.route("/application/<int:application_id>/select", methods=["POST"])
@login_required
@company_required
def select_application_view(application_id):

    application = ApplicationService.get_application_by_id(application_id)

    if not application:
        abort(404)

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.select_application(application_id)

    if result.get("error"):
        flash(result["error"], "danger")
    else:
        flash("Candidate selected successfully.", "success")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )


# ==========================================================
# REJECT
# ==========================================================

@company_bp.route("/application/<int:application_id>/reject", methods=["POST"])
@login_required
@company_required
def reject_application_view(application_id):

    application = ApplicationService.get_application_by_id(application_id)

    if not application:
        abort(404)

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.reject_application(application_id)

    if result.get("error"):
        flash(result["error"], "danger")
    else:
        flash("Candidate rejected.", "info")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )

"""

# ==========================================================
# SHORTLIST
# ==========================================================

@company_bp.route("/application/<int:application_id>/shortlist", methods=["POST"])
@login_required
@company_required
def shortlist_application_view(application_id):

    result = ApplicationService.get_application_by_id(application_id)

    if not result["success"]:
        abort(404)

    application = result["data"]

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.shortlist_application(application_id)

    if not result["success"]:
        flash(result["message"], "danger")
    else:
        flash("Candidate shortlisted successfully.", "success")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )

# ==========================================================
# SELECT
# ==========================================================

@company_bp.route("/application/<int:application_id>/select", methods=["POST"])
@login_required
@company_required
def select_application_view(application_id):

    result = ApplicationService.get_application_by_id(application_id)

    if not result["success"]:
        abort(404)

    application = result["data"]

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.select_application(application_id)

    if not result["success"]:
        flash(result["message"], "danger")
    else:
        flash("Candidate selected successfully.", "success")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )

# ==========================================================
# REJECT
# ==========================================================

@company_bp.route("/application/<int:application_id>/reject", methods=["POST"])
@login_required
@company_required
def reject_application_view(application_id):

    result = ApplicationService.get_application_by_id(application_id)

    if not result["success"]:
        abort(404)

    application = result["data"]

    if application.drive.company_id != current_user.company.id:
        abort(403)

    result = ApplicationService.reject_application(application_id)

    if not result["success"]:
        flash(result["message"], "danger")
    else:
        flash("Candidate rejected.", "info")

    return redirect(
        url_for("company.view_applicants_view", drive_id=application.drive_id)
    )


# ==========================================================
# COMPANY PROFILE
# ==========================================================

@company_bp.route("/profile", methods=["GET", "POST"])
@login_required
@company_required
def company_profile_view():

    company = current_user.company

    if request.method == "POST":

        company.company_name = request.form.get("company_name")
        company.hr_email = request.form.get("hr_email")
        company.website = request.form.get("website")

        db.session.commit()

        flash("Profile updated successfully.", "success")
        return redirect(url_for("company.company_profile_view"))

    return render_template(
        "company/profile.html",
        company=company,
    )
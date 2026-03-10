from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
)
from flask_login import login_required, current_user

from app.decorators import student_required
from app.services.application_service import ApplicationService
from app.services.drive_service import DriveService
from app.services.student_service import StudentService
from app.utils.constants import APPLICATION_SELECTED


student_bp = Blueprint("student", __name__, url_prefix="/student")



# ----------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------

@student_bp.route("/dashboard")
@login_required
@student_required
def student_dashboard_view():

    student = current_user.student

    dashboard_data = StudentService.get_student_dashboard_data(student.id)
    return render_template(
        "student/dashboard.html",
        **dashboard_data
    )


    '''
    approved_drives = DriveService.get_approved_drives()
    applications = ApplicationService.get_student_applications(student.id)

    applied_drive_ids = {app.drive_id for app in applications}
    selected_count = sum(
        1 for app in applications if app.status == "selected"
    )

    return render_template(
        "student/dashboard.html",
        student=student,
        available_drives_count=len(approved_drives),
        applied_drives_count=len(applications),
        selected_count=selected_count,
        recent_applications=applications[:5],
        approved_drives=approved_drives,
        applied_drive_ids=applied_drive_ids,
    )
    '''


# ----------------------------------------------------------
# APPLY TO DRIVE
# ----------------------------------------------------------

@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@login_required
@student_required
def apply_to_drive_view(drive_id):

    student = current_user.student

    result = ApplicationService.apply_to_drive(student.id, drive_id)

    if not result["success"]:
        flash(result["message"], "danger")
        # flash( message, category in bootstrap templates: success, info, warning, danger )
    else:
        flash("Successfully applied to the placement drive.", "success")

    return redirect(url_for("student.student_dashboard_view"))


# ----------------------------------------------------------
# MY APPLICATIONS
# ----------------------------------------------------------

@student_bp.route("/my-applications")
@login_required
@student_required
def my_applications_view():

    student = current_user.student

    applications = ApplicationService.get_student_applications(student.id)

    return render_template(
        "student/my_applications.html",
        applications=applications,
    )


# ----------------------------------------------------------
# PLACEMENT HISTORY
# ----------------------------------------------------------

@student_bp.route("/placement-history")
@login_required
@student_required
def placement_history_view():

    student = current_user.student

    history_records = ApplicationService.get_student_placement_history(
        student.id
    )

    return render_template(
        "student/placement_history.html",
        history_records=history_records,
    )

# ----------------------------------------------------------
# Newly added route for student profile

@student_bp.route("/profile")
@login_required
@student_required
def student_profile_view():

    student = current_user.student

    return render_template(
        "student/profile.html",
        student=student
    )

# Profile Update
@student_bp.route("/profile/update", methods=["POST"])
@login_required
@student_required
def update_student_profile_view():

    if request.method != "POST":
        return redirect(url_for("student.student_profile_view"))

    student = current_user.student

    result = StudentService.update_student_profile(
        student.id,
        request.form
    )

    if result["error"]:
        flash(result["error"], "danger")
    else:
        flash("Profile updated successfully", "success")

    return redirect(url_for("student.student_profile_view"))

# Upload Resume
@student_bp.route("/upload-resume", methods=["POST"])
@login_required
@student_required
def upload_resume_view():

    student = current_user.student

    file = request.files.get("resume")

    result = StudentService.upload_resume(student.id, file)

    if result["error"]:
        flash(result["error"], "danger")
    else:
        flash("Resume uploaded successfully", "success")

    return redirect(url_for("student.student_profile_view"))
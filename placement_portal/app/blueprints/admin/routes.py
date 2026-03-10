from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.decorators import admin_required
from app.services.approval_service import ApprovalService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ==========================================================
# DASHBOARD
# ==========================================================

@admin_bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard_view():

    stats = ApprovalService.get_admin_dashboard_stats()

    return render_template(
        "admin/dashboard.html",
        total_students=stats["total_students"],
        total_companies=stats["total_companies"],
        total_drives=stats["total_drives"],
        total_applications=stats["total_applications"],
    )


# ==========================================================
# PENDING COMPANIES
# ==========================================================

@admin_bp.route("/pending-companies")
@login_required
@admin_required
def pending_companies_view():

    print(" Companies are:")


    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    companies, pagination = ApprovalService.get_pending_companies(q, page)

    return render_template(
        "admin/pending_companies.html",
        pending_companies=companies,
        pagination=pagination, #pagination is an object that contains information about the pagination, such as the current page, total pages, etc.
    )


@admin_bp.route("/approve-company/<int:company_id>", methods=["POST"])
@login_required
@admin_required
def approve_company_view(company_id):

    result = ApprovalService.approve_company(company_id)
    flash(result["message"], "success" if result["success"] else "danger")

    return redirect(url_for("admin.pending_companies_view"))


@admin_bp.route("/reject-company/<int:company_id>", methods=["POST"])
@login_required
@admin_required
def reject_company_view(company_id):

    result = ApprovalService.reject_company(company_id)
    flash(result["message"], "warning" if result["success"] else "danger")

    return redirect(url_for("admin.pending_companies_view"))


# ==========================================================
# PENDING DRIVES
# ==========================================================

@admin_bp.route("/pending-drives")
@login_required
@admin_required
def pending_drives_view():

    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    drives, pagination = ApprovalService.get_pending_drives(q, page)

    return render_template(
        "admin/pending_drives.html",
        pending_drives=drives,
        pagination=pagination,
    )


@admin_bp.route("/approve-drive/<int:drive_id>", methods=["POST"])
@login_required
@admin_required
def approve_drive_view(drive_id):

    result = ApprovalService.approve_drive(drive_id)
    flash(result["message"], "success" if result["success"] else "danger")

    return redirect(url_for("admin.pending_drives_view"))


@admin_bp.route("/reject-drive/<int:drive_id>", methods=["POST"])
@login_required
@admin_required
def reject_drive_view(drive_id):

    result = ApprovalService.reject_drive(drive_id)
    flash(result["message"], "warning" if result["success"] else "danger")

    return redirect(url_for("admin.pending_drives_view"))


# ==========================================================
# MANAGE STUDENTS
# ==========================================================

@admin_bp.route("/manage-students")
@login_required
@admin_required
def manage_students_view():

    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    students, pagination = ApprovalService.get_all_students(q, page)

    return render_template(
        "admin/manage_students.html",
        students=students,
        pagination=pagination,
    )


@admin_bp.route("/blacklist-student/<int:student_id>", methods=["POST"])
@login_required
@admin_required
def blacklist_student_view(student_id):

    result = ApprovalService.blacklist_student(student_id)
    flash(result["message"], "warning" if result["success"] else "danger")

    return redirect(url_for("admin.manage_students_view"))


@admin_bp.route("/activate-student/<int:student_id>", methods=["POST"])
@login_required
@admin_required
def activate_student_view(student_id):

    result = ApprovalService.activate_student(student_id)
    flash(result["message"], "success" if result["success"] else "danger")

    return redirect(url_for("admin.manage_students_view"))


# ==========================================================
# MANAGE COMPANIES
# ==========================================================

@admin_bp.route("/manage-companies")
@login_required
@admin_required
def manage_companies_view():

    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    companies, pagination = ApprovalService.get_all_companies(q, page)

    return render_template(
        "admin/manage_companies.html",
        companies=companies,
        pagination=pagination,
    )


@admin_bp.route("/blacklist-company/<int:company_id>", methods=["POST"])
@login_required
@admin_required
def blacklist_company_view(company_id):

    result = ApprovalService.blacklist_company(company_id)
    flash(result["message"], "warning" if result["success"] else "danger")

    return redirect(url_for("admin.manage_companies_view"))


@admin_bp.route("/activate-company/<int:company_id>", methods=["POST"])
@login_required
@admin_required
def activate_company_view(company_id):

    result = ApprovalService.activate_company(company_id)
    flash(result["message"], "success" if result["success"] else "danger")

    return redirect(url_for("admin.manage_companies_view"))


# ==========================================================
# APPLICATIONS OVERVIEW (NEW – REQUIRED BY TEMPLATES)
# ==========================================================

@admin_bp.route("/applications")
@login_required
@admin_required
def view_all_applications_view():

    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    applications, pagination = ApprovalService.get_all_applications(q, page)

    return render_template(
        "admin/applications.html",
        applications=applications,
        pagination=pagination,
    )


# ==========================================================
# REPORTS
# ==========================================================

@admin_bp.route("/reports")
@login_required
@admin_required
def reports_view():

    stats = ApprovalService.get_reports_stats()

    return render_template(
        "admin/reports.html",
        total_selected=stats["total_selected"],
        total_rejected=stats["total_rejected"],
        selection_ratio=stats["selection_ratio"],
    )
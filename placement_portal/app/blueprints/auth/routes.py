from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.utils.constants import ADMIN, COMPANY, STUDENT


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ----------------------------------------------------------
# REGISTER STUDENT
# ----------------------------------------------------------

@auth_bp.route("/register-student", methods=["GET", "POST"])
def register_student_view():

    if request.method == "POST":

        result = AuthService.register_student(request.form)

        if result["error"]:
            return render_template(
                "auth/register_student.html",
                error=result["error"],
                form_data=request.form,
            )

        return redirect(url_for("auth.login_view"))

    return render_template("auth/register_student.html", error=None)


# ----------------------------------------------------------
# REGISTER COMPANY
# ----------------------------------------------------------

@auth_bp.route("/register-company", methods=["GET", "POST"])
def register_company_view():

    if request.method == "POST":

        result = AuthService.register_company(request.form)

        if result["error"]:
            return render_template(
                "auth/register_company.html",
                error=result["error"],
                form_data=request.form,
            )

        return redirect(url_for("auth.login_view"))

    return render_template("auth/register_company.html", error=None)


# ----------------------------------------------------------
# LOGIN
# ----------------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login_view():

    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    if request.method == "POST":

        result = AuthService.authenticate_user(
            request.form.get("email"),
            request.form.get("password"),
        )

        if result["error"]:
            return render_template(
                "auth/login.html",
                error=result["error"],
            )

        user = result["user"]
        login_user(user)

        return _redirect_by_role(user)

    return render_template("auth/login.html", error=None)


# ----------------------------------------------------------
# LOGOUT
# ----------------------------------------------------------

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout_view():

    logout_user()
    return redirect(url_for("auth.login_view"))


# ----------------------------------------------------------
# ROLE REDIRECTION
# ----------------------------------------------------------

def _redirect_by_role(user):

    if user.role == ADMIN:
        return redirect(url_for("admin.admin_dashboard_view"))

    if user.role == COMPANY:
        return redirect(url_for("company.company_dashboard_view"))

    if user.role == STUDENT:
        return redirect(url_for("student.student_dashboard_view"))

    return redirect(url_for("auth.login_view"))
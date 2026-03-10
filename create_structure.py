import os

BASE = "placement_portal"

DIRS = [
    "instance",
    "scripts",
    "app",
    "app/errors",
    "app/uploads",
    "app/uploads/resumes",
    "app/models",
    "app/services",
    "app/utils",
    "app/static",
    "app/static/css",
    "app/static/images",
    "app/templates",
    "app/templates/auth",
    "app/templates/admin",
    "app/templates/company",
    "app/templates/student",
    "app/blueprints",
    "app/blueprints/auth",
    "app/blueprints/admin",
    "app/blueprints/company",
    "app/blueprints/student",
    "app/blueprints/api",
]

FILES = [
    # root
    "run.py",
    "config.py",
    "requirements.txt",

    # instance
    "instance/placement.db",

    # scripts
    "scripts/seed_admin.py",

    # app core
    "app/__init__.py",
    "app/extensions.py",
    "app/decorators.py",

    # errors
    "app/errors/__init__.py",
    "app/errors/handlers.py",

    # models
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/admin.py",
    "app/models/company.py",
    "app/models/student.py",
    "app/models/placement_drive.py",
    "app/models/application.py",
    "app/models/notification.py",

    # services
    "app/services/auth_service.py",
    "app/services/approval_service.py",
    "app/services/application_service.py",

    # utils
    "app/utils/constants.py",
    "app/utils/validators.py",

    # static
    "app/static/css/style.css",

    # templates
    "app/templates/base.html",

    # auth templates
    "app/templates/auth/login.html",
    "app/templates/auth/register_student.html",
    "app/templates/auth/register_company.html",

    # admin templates
    "app/templates/admin/dashboard.html",
    "app/templates/admin/pending_companies.html",
    "app/templates/admin/pending_drives.html",
    "app/templates/admin/manage_students.html",
    "app/templates/admin/manage_companies.html",
    "app/templates/admin/applications.html",
    "app/templates/admin/reports.html",
    "app/templates/admin/_stats_cards.html",
    "app/templates/admin/_search_panel.html",
    "app/templates/admin/_notifications.html",
    "app/templates/admin/_admin_sidebar.html",

    # company templates
    "app/templates/company/dashboard.html",
    "app/templates/company/create_drive.html",
    "app/templates/company/my_drives.html",
    "app/templates/company/drive_detail.html",
    "app/templates/company/applications.html",
    "app/templates/company/shortlisted.html",
    "app/templates/company/profile.html",
    "app/templates/company/_stats_cards.html",
    "app/templates/company/_company_profile_card.html",
    "app/templates/company/_notifications.html",
    "app/templates/company/_company_sidebar.html",

    # student templates
    "app/templates/student/dashboard.html",
    "app/templates/student/available_drives.html",
    "app/templates/student/my_applications.html",
    "app/templates/student/placement_history.html",
    "app/templates/student/profile.html",
    "app/templates/student/upload_resume.html",
    "app/templates/student/_stats_cards.html",
    "app/templates/student/_drive_table.html",
    "app/templates/student/_profile_snapshot.html",
    "app/templates/student/_notifications.html",
    "app/templates/student/_student_sidebar.html",

    # blueprints
    "app/blueprints/auth/routes.py",
    "app/blueprints/admin/routes.py",
    "app/blueprints/company/routes.py",
    "app/blueprints/student/routes.py",
    "app/blueprints/api/routes.py",
]

def main():
    os.makedirs(BASE, exist_ok=True)

    for d in DIRS:
        os.makedirs(os.path.join(BASE, d), exist_ok=True)

    for f in FILES:
        path = os.path.join(BASE, f)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8"):
                pass

    print("✅ Exact directory structure created successfully (no files skipped).")

if __name__ == "__main__":
    main()

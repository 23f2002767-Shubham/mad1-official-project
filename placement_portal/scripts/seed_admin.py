'''
Admin is created programatically for safety and security reasons
since the Industry Interaction Cell / Placement Cell coordinators are generally a team of few people ,
their credentials are seeded manually via this script
'''

from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    existing_admin = User.query.filter_by(role="admin").first()

    if not existing_admin:
        admin = User(
            email="admin@institute.edu",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")
    else:
        print("Admin already exists.")

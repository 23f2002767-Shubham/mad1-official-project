from app.extensions import db
from flask_login import UserMixin
from app.utils.constants import ADMIN, COMPANY, STUDENT


class User(db.Model, UserMixin):
    __tablename__ = "users"

    __table_args__ = (
        db.CheckConstraint(
            f"role IN ('{ADMIN}', '{COMPANY}', '{STUDENT}')",
            name="valid_role"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    #Email is frequently queried during login , Adding index improves lookup performance
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
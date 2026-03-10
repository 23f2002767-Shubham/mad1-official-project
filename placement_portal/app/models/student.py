from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    # -------------------------------------------------
    # Core Fields
    # -------------------------------------------------

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    student_id = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    name = db.Column(db.String(100), nullable=False)

    branch = db.Column(db.String(50), nullable=False)

    cgpa = db.Column(db.Float, nullable=False)

    resume_path = db.Column(db.String(255), nullable=True)

    is_resume_uploaded = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    # -------------------------------------------------
    # Governance Fields
    # -------------------------------------------------

    is_blacklisted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    user = db.relationship(
        "User",
        backref=db.backref("student", uselist=False),
        passive_deletes=True,
    )

    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # -------------------------------------------------

    def __repr__(self):
        return (
            f"<Student id={self.id} "
            f"student_id={self.student_id} "
            f"name={self.name} "
            f"blacklisted={self.is_blacklisted}>"
        )
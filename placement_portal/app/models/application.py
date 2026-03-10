from app.extensions import db
from app.utils.constants import (
    APPLICATION_APPLIED,
    APPLICATION_SHORTLISTED,
    APPLICATION_SELECTED,
    APPLICATION_REJECTED,
)


class Application(db.Model):
    __tablename__ = "applications"

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="unique_application",
        ),
        db.CheckConstraint(
            f"status IN ('{APPLICATION_APPLIED}', "
            f"'{APPLICATION_SHORTLISTED}', "
            f"'{APPLICATION_SELECTED}', "
            f"'{APPLICATION_REJECTED}')",
            name="valid_application_status",
        ),
    )

    # -------------------------------------------------
    # Core Fields
    # -------------------------------------------------

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default=APPLICATION_APPLIED,
    )

    applied_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    student = db.relationship(
        "Student",
        back_populates="applications",
        passive_deletes=True,
    )

    drive = db.relationship(
        "PlacementDrive",
        back_populates="applications",
        passive_deletes=True,
    )

    # -------------------------------------------------

    def __repr__(self):
        return (
            f"<Application id={self.id} "
            f"student_id={self.student_id} "
            f"drive_id={self.drive_id} "
            f"status={self.status}>"
        )
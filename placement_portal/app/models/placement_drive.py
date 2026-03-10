from app.extensions import db
from app.utils.constants import (
    DRIVE_PENDING,
    DRIVE_APPROVED,
    DRIVE_REJECTED,
    DRIVE_CLOSED,
)


class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    __table_args__ = (
        db.CheckConstraint(
            f"status IN ("
            f"'{DRIVE_PENDING}', "
            f"'{DRIVE_APPROVED}', "
            f"'{DRIVE_REJECTED}', "
            f"'{DRIVE_CLOSED}'"
            f")",
            name="valid_drive_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.String(200), nullable=False)

    application_deadline = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default=DRIVE_PENDING,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    approved_at = db.Column(
        db.DateTime,
        nullable=True,
    )

# Relationships

#company is 
    company = db.relationship(
        "Company",
        back_populates="drives",
        passive_deletes=True,
    )

    applications = db.relationship(
        "Application",
        back_populates="drive",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<PlacementDrive id={self.id} "
            f"title={self.job_title} "
            f"status={self.status}>"
        )
from app.extensions import db
from app.utils.constants import (
    COMPANY_PENDING,
    COMPANY_APPROVED,
    COMPANY_REJECTED,
)


class Company(db.Model):
    __tablename__ = "companies"

    __table_args__ = (
        db.CheckConstraint(
            f"approval_status IN ('{COMPANY_PENDING}', "
            f"'{COMPANY_APPROVED}', "
            f"'{COMPANY_REJECTED}')",
            name="valid_company_status",
        ),
    )

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

    company_name = db.Column(db.String(150), nullable=False, index=True)

    hr_email = db.Column(db.String(120), nullable=False)

    website = db.Column(db.String(255), nullable=True)

    # -------------------------------------------------
    # Governance Fields
    # -------------------------------------------------

    approval_status = db.Column(
        db.String(20),
        nullable=False,
        default=COMPANY_PENDING,
    )

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

    approved_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    user = db.relationship(
        "User",
        backref=db.backref("company", uselist=False),
        passive_deletes=True,
    )

    drives = db.relationship(
        "PlacementDrive",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    # -------------------------------------------------

    def __repr__(self):
        return (
            f"<Company id={self.id} "
            f"name={self.company_name} "
            f"status={self.approval_status} "
            f"blacklisted={self.is_blacklisted}>"
        )
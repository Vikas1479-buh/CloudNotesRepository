from enum import Enum

from app.extensions import db
from app.models.base import BaseModel


class ApprovalStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class Note(BaseModel):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    storage_path = db.Column(
        db.String(255),
        nullable=False
    )

    file_url = db.Column(
        db.Text,
        nullable=False
    )

    file_type = db.Column(
        db.String(20),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        nullable=False
    )

    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    approval_status = db.Column(
        db.Enum(ApprovalStatus),
        default=ApprovalStatus.PENDING,
        nullable=False
    )

    download_count = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    uploader = db.relationship(
        "User",
        backref="notes"
    )

    subject = db.relationship(
        "Subject",
        back_populates="notes"
    )

    def __repr__(self):
        return f"<Note {self.title}>"
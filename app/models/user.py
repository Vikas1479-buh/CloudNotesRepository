from enum import Enum

from flask_login import UserMixin

from app.extensions import db
from app.models.base import BaseModel


class UserRole(str, Enum):
    ADMIN = "Admin"
    FACULTY = "Faculty"
    STUDENT = "Student"


class User(UserMixin, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.STUDENT,
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship(
        "Department",
        back_populates="users"
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.email}>"
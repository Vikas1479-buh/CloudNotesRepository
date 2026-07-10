from app.extensions import db
from app.models.base import BaseModel


class Subject(BaseModel):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship(
        "Department",
        back_populates="subjects"
    )

    notes = db.relationship(
        "Note",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Subject {self.code}>"
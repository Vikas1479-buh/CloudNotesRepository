from app.extensions import db
from app.models.base import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    users = db.relationship(
        "User",
        back_populates="department"
    )

    subjects = db.relationship(
        "Subject",
        back_populates="department"
    )

    def __repr__(self):
        return f"<Department {self.name}>"
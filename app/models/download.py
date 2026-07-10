from app.extensions import db
from app.models.base import BaseModel


class Download(BaseModel):
    __tablename__ = "downloads"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    note_id = db.Column(
        db.Integer,
        db.ForeignKey("notes.id"),
        nullable=False
    )

    user = db.relationship("User", backref="downloads")
    note = db.relationship("Note", backref="downloads")
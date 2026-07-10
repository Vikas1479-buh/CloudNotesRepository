from flask import render_template
from flask_login import current_user

from app.models import User, Department, Subject, Note
from app.utils.decorators import admin_required

from . import admin


@admin.route("/dashboard")
@admin_required
def dashboard():

    total_users = User.query.count()
    total_departments = Department.query.count()
    total_subjects = Subject.query.count()
    total_notes = Note.query.count()

    recent_notes = (
        Note.query
        .order_by(Note.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_departments=total_departments,
        total_subjects=total_subjects,
        total_notes=total_notes,
        recent_notes=recent_notes
    )


@admin.route("/profile")
@admin_required
def profile():

    return render_template(
        "admin/profile.html",
        user=current_user
    )
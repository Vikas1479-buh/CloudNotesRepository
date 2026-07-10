from flask import render_template
from flask_login import current_user

from app.utils.decorators import faculty_required
from . import faculty


@faculty.route("/dashboard")
@faculty_required
def dashboard():

    return render_template(
        "faculty/dashboard.html",
        user=current_user
    )


@faculty.route("/profile")
@faculty_required
def profile():

    return render_template(
        "faculty/profile.html",
        user=current_user
    )
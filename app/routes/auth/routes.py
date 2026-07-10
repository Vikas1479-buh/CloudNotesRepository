from flask import render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    logout_user,
    current_user
)
from werkzeug.security import check_password_hash

from app.models import User, UserRole

from . import auth


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == UserRole.ADMIN:
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == UserRole.FACULTY:
            return redirect(url_for("faculty.dashboard"))

        elif current_user.role == UserRole.STUDENT:
            return redirect(url_for("student.dashboard"))

    if request.method == "POST":

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            if user.role == UserRole.ADMIN:
                return redirect(url_for("admin.dashboard"))

            elif user.role == UserRole.FACULTY:
                return redirect(url_for("faculty.dashboard"))

            elif user.role == UserRole.STUDENT:
                return redirect(url_for("student.dashboard"))

        flash(
            "Invalid Email or Password",
            "danger"
        )

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(url_for("auth.login"))
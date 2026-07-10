from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User, UserRole, Department
from app.utils.decorators import admin_required

from . import admin


@admin.route("/users")
@admin_required
def users():

    search = request.args.get("search", "").strip()

    role = request.args.get("role", "")

    department = request.args.get("department", "")

    status = request.args.get("status", "")

    query = User.query

    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    if role:
        query = query.filter(User.role == UserRole(role))

    if department:
        query = query.filter(
            User.department_id == int(department)
        )

    if status:

        active = status == "Active"

        query = query.filter(
            User.is_active == active
        )

    users = query.order_by(
        User.full_name
    ).all()

    departments = Department.query.order_by(
        Department.name
    ).all()

    return render_template(
        "admin/users.html",
        users=users,
        departments=departments,
        roles=list(UserRole),
        search=search,
        selected_role=role,
        selected_department=department,
        selected_status=status
    )


@admin.route("/users/add", methods=["GET", "POST"])
@admin_required
def add_user():

    departments = Department.query.order_by(
        Department.name
    ).all()

    roles = list(UserRole)

    if request.method == "POST":

        full_name = request.form.get("full_name").strip()

        email = request.form.get("email").strip().lower()

        password = request.form.get("password")

        role = request.form.get("role")

        department_id = request.form.get("department")

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect("/admin/users/add")

        user = User(

            full_name=full_name,

            email=email,

            password_hash=generate_password_hash(
                password
            ),

            role=UserRole(role),

            department_id=department_id

        )

        db.session.add(user)

        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect("/admin/users")

    return render_template(
        "admin/add_user.html",
        departments=departments,
        roles=roles
    )


@admin.route("/users/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_user(id):

    user = User.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name
    ).all()

    roles = list(UserRole)

    if request.method == "POST":

        user.full_name = request.form.get(
            "full_name"
        ).strip()

        user.email = request.form.get(
            "email"
        ).strip().lower()

        user.role = UserRole(
            request.form.get("role")
        )

        user.department_id = request.form.get(
            "department"
        )

        user.is_active = (
            request.form.get("status")
            == "Active"
        )

        password = request.form.get(
            "password"
        )

        if password:

            user.password_hash = generate_password_hash(
                password
            )

        db.session.commit()

        flash(
            "User updated successfully.",
            "success"
        )

        return redirect("/admin/users")

    return render_template(
        "admin/edit_user.html",
        user=user,
        departments=departments,
        roles=roles
    )


@admin.route("/users/delete/<int:id>")
@admin_required
def delete_user(id):

    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect("/admin/users")
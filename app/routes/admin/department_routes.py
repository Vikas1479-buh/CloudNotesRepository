from flask import render_template, request, redirect, flash
from flask_login import login_required

from app.extensions import db
from app.models import Department
from . import admin


@admin.route("/departments")
@login_required
def departments():

    departments = Department.query.order_by(
        Department.name
    ).all()

    return render_template(
        "admin/departments.html",
        departments=departments
    )


@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():

    if request.method == "POST":

        name = request.form.get("name").strip()

        existing = Department.query.filter_by(name=name).first()

        if existing:
            flash("Department already exists.", "danger")
            return redirect("/admin/departments/add")

        department = Department(name=name)

        db.session.add(department)
        db.session.commit()

        flash("Department added successfully.", "success")

        return redirect("/admin/departments")

    return render_template("admin/add_department.html")


@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):

    department = Department.query.get_or_404(id)

    if request.method == "POST":

        department.name = request.form.get("name").strip()

        db.session.commit()

        flash("Department updated successfully.", "success")

        return redirect("/admin/departments")

    return render_template(
        "admin/edit_department.html",
        department=department
    )


@admin.route("/departments/delete/<int:id>")
@login_required
def delete_department(id):

    department = Department.query.get_or_404(id)

    if department.users or department.subjects:
        flash(
            "Cannot delete department because it has users or subjects assigned.",
            "danger"
        )
        return redirect("/admin/departments")

    db.session.delete(department)
    db.session.commit()

    flash("Department deleted successfully.", "success")

    return redirect("/admin/departments")
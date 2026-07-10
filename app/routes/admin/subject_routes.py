from flask import render_template, request, redirect, flash

from app.extensions import db
from app.models import Subject, Department
from app.utils.decorators import admin_required

from . import admin


@admin.route("/subjects")
@admin_required
def subjects():

    search = request.args.get("search", "").strip()

    semester = request.args.get("semester", "")

    department = request.args.get("department", "")

    query = Subject.query

    if search:
        query = query.filter(
            Subject.name.ilike(f"%{search}%")
        )

    if semester:
        query = query.filter(
            Subject.semester == int(semester)
        )

    if department:
        query = query.filter(
            Subject.department_id == int(department)
        )

    subjects = (
        query.order_by(
            Subject.semester,
            Subject.name
        ).all()
    )

    departments = Department.query.order_by(
        Department.name
    ).all()

    return render_template(
        "admin/subjects.html",
        subjects=subjects,
        departments=departments,
        search=search,
        selected_semester=semester,
        selected_department=department
    )


@admin.route("/subjects/add", methods=["GET", "POST"])
@admin_required
def add_subject():

    departments = Department.query.order_by(
        Department.name
    ).all()

    if request.method == "POST":

        code = request.form.get("code").strip()
        name = request.form.get("name").strip()
        semester = request.form.get("semester")
        department_id = request.form.get("department")

        existing = Subject.query.filter_by(code=code).first()

        if existing:
            flash("Subject code already exists.", "danger")
            return redirect("/admin/subjects/add")

        subject = Subject(
            code=code,
            name=name,
            semester=semester,
            department_id=department_id
        )

        db.session.add(subject)
        db.session.commit()

        flash("Subject added successfully.", "success")

        return redirect("/admin/subjects")

    return render_template(
        "admin/add_subject.html",
        departments=departments
    )


@admin.route("/subjects/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_subject(id):

    subject = Subject.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name
    ).all()

    if request.method == "POST":

        subject.code = request.form.get("code").strip()
        subject.name = request.form.get("name").strip()
        subject.semester = request.form.get("semester")
        subject.department_id = request.form.get("department")

        db.session.commit()

        flash("Subject updated successfully.", "success")

        return redirect("/admin/subjects")

    return render_template(
        "admin/edit_subject.html",
        subject=subject,
        departments=departments
    )


@admin.route("/subjects/delete/<int:id>")
@admin_required
def delete_subject(id):

    subject = Subject.query.get_or_404(id)

    if subject.notes:
        flash(
            "Cannot delete subject because notes exist.",
            "danger"
        )
        return redirect("/admin/subjects")

    db.session.delete(subject)
    db.session.commit()

    flash("Subject deleted successfully.", "success")

    return redirect("/admin/subjects")
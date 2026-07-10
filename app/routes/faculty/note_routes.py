from flask import (
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    abort,
    url_for
)

from flask_login import current_user

import os

from app.extensions import db
from app.models import Subject, Note, ApprovalStatus
from app.utils.decorators import faculty_required
from app.utils.supabase_storage import upload_file, delete_file

from . import faculty


ALLOWED_EXTENSIONS = {
    ".pdf": "PDF",
    ".ppt": "PPT",
    ".pptx": "PPTX"
}


@faculty.route("/upload-note", methods=["GET", "POST"])
@faculty_required
def upload_note():

    subjects = (
        Subject.query.filter_by(
            department_id=current_user.department_id
        )
        .order_by(
            Subject.semester,
            Subject.name
        )
        .all()
    )

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        subject_id = request.form.get("subject")

        uploaded_file = request.files.get("note_file")

        if not uploaded_file or uploaded_file.filename == "":
            flash("Please choose a file.", "danger")
            return redirect(url_for("faculty.upload_note"))

        extension = os.path.splitext(
            uploaded_file.filename
        )[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            flash(
                "Only PDF, PPT and PPTX files are allowed.",
                "danger"
            )
            return redirect(url_for("faculty.upload_note"))

        try:

            result = upload_file(uploaded_file)

            note = Note(
                title=title,
                description=description,
                subject_id=int(subject_id),
                uploaded_by=current_user.id,
                file_name=uploaded_file.filename,
                storage_path=result["path"],
                file_url=result["url"],
                file_type=ALLOWED_EXTENSIONS[extension],
                file_size=uploaded_file.content_length or 0,
                approval_status=ApprovalStatus.PENDING
            )

            db.session.add(note)
            db.session.commit()

            flash(
                "Note uploaded successfully.",
                "success"
            )

            return redirect(
                url_for("faculty.my_notes")
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"Upload failed : {str(e)}",
                "danger"
            )

            return redirect(
                url_for("faculty.upload_note")
            )

    return render_template(
        "faculty/upload_note.html",
        subjects=subjects
    )


@faculty.route("/subjects/<int:semester>")
@faculty_required
def get_subjects(semester):

    subjects = (
        Subject.query.filter_by(
            department_id=current_user.department_id,
            semester=semester
        )
        .order_by(
            Subject.name
        )
        .all()
    )

    return jsonify([
        {
            "id": subject.id,
            "code": subject.code,
            "name": subject.name
        }
        for subject in subjects
    ])
@faculty.route("/my-notes")
@faculty_required
def my_notes():

    search = request.args.get("search", "").strip()
    semester = request.args.get("semester", "")

    query = Note.query.filter_by(
        uploaded_by=current_user.id
    )

    if search:
        query = query.filter(
            Note.title.ilike(f"%{search}%")
        )

    if semester:
        query = query.join(Subject).filter(
            Subject.semester == int(semester)
        )

    notes = (
        query.order_by(
            Note.created_at.desc()
        )
        .all()
    )

    return render_template(
        "faculty/my_notes.html",
        notes=notes,
        search=search,
        selected_semester=semester
    )


@faculty.route("/edit-note/<int:id>", methods=["GET", "POST"])
@faculty_required
def edit_note(id):

    note = Note.query.get_or_404(id)

    if note.uploaded_by != current_user.id:
        abort(403)

    subjects = (
        Subject.query.filter_by(
            department_id=current_user.department_id
        )
        .order_by(
            Subject.semester,
            Subject.name
        )
        .all()
    )

    if request.method == "POST":

        note.title = request.form.get("title").strip()
        note.description = request.form.get("description").strip()
        note.subject_id = request.form.get("subject")

        db.session.commit()

        flash(
            "Note updated successfully.",
            "success"
        )

        return redirect(
            url_for("faculty.my_notes")
        )

    return render_template(
        "faculty/edit_note.html",
        note=note,
        subjects=subjects
    )


@faculty.route("/preview/<int:id>")
@faculty_required
def preview_note(id):

    note = Note.query.get_or_404(id)

    if note.uploaded_by != current_user.id:
        abort(403)

    return redirect(note.file_url)


@faculty.route("/download/<int:id>")
@faculty_required
def download_note(id):

    note = Note.query.get_or_404(id)

    if note.uploaded_by != current_user.id:
        abort(403)

    note.download_count += 1

    db.session.commit()

    return redirect(note.file_url)

@faculty.route("/delete-note/<int:id>")
@faculty_required
def delete_note(id):

    note = Note.query.get_or_404(id)

    if note.uploaded_by != current_user.id:
        abort(403)

    try:

        if note.storage_path:
            delete_file(note.storage_path)

    except Exception as e:
        print(f"Supabase delete error: {e}")

    db.session.delete(note)
    db.session.commit()

    flash(
        "Note deleted successfully.",
        "success"
    )

    return redirect(
        url_for("faculty.my_notes")
    )
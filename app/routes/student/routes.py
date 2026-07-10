from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort
)

from flask_login import current_user

from app.extensions import db
from app.models import (
    Note,
    Subject,
    Bookmark,
    Download
)
from app.utils.decorators import student_required

from . import student


@student.route("/dashboard")
@student_required
def dashboard():

    semester = request.args.get("semester", "")
    subject = request.args.get("subject", "")
    search = request.args.get("search", "")

    query = Note.query.join(Subject)

    if semester:
        query = query.filter(
            Subject.semester == int(semester)
        )

    if subject:
        query = query.filter(
            Subject.id == int(subject)
        )

    if search:
        query = query.filter(
            Note.title.ilike(f"%{search}%")
        )

    notes = (
        query.order_by(
            Note.created_at.desc()
        )
        .all()
    )

    subjects = (
        Subject.query.order_by(
            Subject.semester,
            Subject.name
        )
        .all()
    )

    bookmarked_notes = {
        bookmark.note_id
        for bookmark in Bookmark.query.filter_by(
            user_id=current_user.id
        ).all()
    }

    return render_template(
        "student/dashboard.html",
        notes=notes,
        subjects=subjects,
        search=search,
        selected_semester=semester,
        selected_subject=subject,
        bookmarked_notes=bookmarked_notes
    )


@student.route("/download/<int:id>")
@student_required
def download_note(id):

    note = Note.query.get_or_404(id)

    note.download_count += 1

    history = Download(
        user_id=current_user.id,
        note_id=note.id
    )

    db.session.add(history)
    db.session.commit()

    return redirect(note.file_url)


@student.route("/bookmark/<int:id>")
@student_required
def bookmark_note(id):

    note = Note.query.get_or_404(id)

    bookmark = Bookmark.query.filter_by(
        user_id=current_user.id,
        note_id=note.id
    ).first()

    if bookmark:

        db.session.delete(bookmark)

    else:

        bookmark = Bookmark(
            user_id=current_user.id,
            note_id=note.id
        )

        db.session.add(bookmark)

    db.session.commit()

    return redirect(
        url_for("student.dashboard")
    )


@student.route("/profile")
@student_required
def profile():

    return render_template(
        "student/profile.html",
        user=current_user
    )

@student.route("/bookmarks")
@student_required
def bookmarks():

    bookmarks = (
        Bookmark.query.filter_by(
            user_id=current_user.id
        )
        .order_by(
            Bookmark.created_at.desc()
        )
        .all()
    )

    return render_template(
        "student/bookmarks.html",
        bookmarks=bookmarks
    )


@student.route("/downloads")
@student_required
def downloads():

    downloads = (
        Download.query.filter_by(
            user_id=current_user.id
        )
        .order_by(
            Download.created_at.desc()
        )
        .all()
    )

    return render_template(
        "student/downloads.html",
        downloads=downloads
    )


@student.route("/subjects/<int:semester>")
@student_required
def subjects(semester):

    subjects = (
        Subject.query.filter_by(
            semester=semester
        )
        .order_by(
            Subject.name
        )
        .all()
    )

    return {
        "subjects": [
            {
                "id": subject.id,
                "code": subject.code,
                "name": subject.name
            }
            for subject in subjects
        ]
    }


@student.route("/preview/<int:id>")
@student_required
def preview(id):

    note = Note.query.get_or_404(id)

    return redirect(note.file_url)
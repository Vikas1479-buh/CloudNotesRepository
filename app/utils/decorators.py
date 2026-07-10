from functools import wraps

from flask import abort
from flask_login import current_user, login_required

from app.models.user import UserRole


def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != UserRole.ADMIN:
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def faculty_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != UserRole.FACULTY:
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def student_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != UserRole.STUDENT:
            abort(403)

        return func(*args, **kwargs)

    return wrapper
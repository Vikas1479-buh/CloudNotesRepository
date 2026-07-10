from flask import Flask, render_template, redirect, url_for
from flask_login import current_user

from config import Config

from app.extensions import db, migrate, login_manager


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User, UserRole

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.faculty import faculty
    from app.routes.student import student

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(faculty)
    app.register_blueprint(student)

    @app.route("/")
    def home():

        if current_user.is_authenticated:

            if current_user.role == UserRole.ADMIN:
                return redirect(url_for("admin.dashboard"))

            elif current_user.role == UserRole.FACULTY:
                return redirect(url_for("faculty.dashboard"))

            elif current_user.role == UserRole.STUDENT:
                return redirect(url_for("student.dashboard"))

        return render_template("index.html")

    return app
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User, Department, UserRole

app = create_app()

with app.app_context():

    department = Department.query.filter_by(name="Computer Science").first()

    if not department:
        department = Department(name="Computer Science")
        db.session.add(department)
        db.session.commit()

    admin = User.query.filter_by(email="admin@cloudnotes.com").first()

    if not admin:
        admin = User(
            full_name="Administrator",
            email="admin@cloudnotes.com",
            password_hash=generate_password_hash("Admin@123"),
            role=UserRole.ADMIN,
            department_id=department.id,
            is_active=True,
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully.")
    else:
        print("Admin already exists.")
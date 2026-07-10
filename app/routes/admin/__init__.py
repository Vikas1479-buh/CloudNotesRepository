from flask import Blueprint

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

from app.routes.admin import routes
from app.routes.admin import department_routes
from app.routes.admin import subject_routes
from app.routes.admin import user_routes
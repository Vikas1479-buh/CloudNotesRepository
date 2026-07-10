from flask import Blueprint

faculty = Blueprint(
    "faculty",
    __name__,
    url_prefix="/faculty"
)

from app.routes.faculty import routes
from app.routes.faculty import note_routes
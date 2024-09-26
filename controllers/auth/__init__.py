from flask import Blueprint

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/auth'
)

from . import routes  # Import routes after creating the blueprint

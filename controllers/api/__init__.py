from flask import Blueprint

admin_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/api'
)

from . import routes  # Import routes after creating the blueprint
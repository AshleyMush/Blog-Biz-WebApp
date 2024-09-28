from flask import Blueprint

user_bp = Blueprint(
    'user_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/user'
)

from . import routes  # Import routes after creating the blueprint

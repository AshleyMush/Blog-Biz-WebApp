from flask import Blueprint

contributor_bp = Blueprint(
    'contributor_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/contrib'
)

from . import routes  # Import routes after creating the blueprint
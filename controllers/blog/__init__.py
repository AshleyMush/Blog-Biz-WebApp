from flask import Blueprint

blog_bp = Blueprint(
    'blog_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
)


from . import routes  # Import routes after creating the blueprint
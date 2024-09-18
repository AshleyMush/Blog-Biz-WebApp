# decorators.py
from flask import abort
from functools import wraps
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the user is authenticated and has the required role
            if not current_user.is_authenticated:
                return abort(403)
            if current_user.role not in roles:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# decorators.py
from flask import g, request, redirect, url_for, abort
from functools import wraps
from flask_login import current_user

def roles_required(*roles):
    """"
    Decorator to check if the user has the required roles"
    param roles: The roles required by the user (str)
    """
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


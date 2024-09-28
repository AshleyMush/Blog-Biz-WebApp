# decorators.py
from flask import g, request, redirect, url_for, abort
from functools import wraps
from flask_login import login_required, current_user
from flask import flash, redirect, url_for

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Admin':
            flash('You do not have permission to access this page.', 'danger')
            #TODO CHANGE THE REDIRECT URL
            return redirect(url_for('main_bp.index'))
        return f(*args, **kwargs)
    return decorated_function


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


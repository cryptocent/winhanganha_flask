from functools import wraps
from flask import abort
from flask_login import login_required, current_user
from project.models import Permission


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_administrator(func):
    return permission_required(Permission.ADMINISTRATOR)(func)
###
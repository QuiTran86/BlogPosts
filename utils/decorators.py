from functools import wraps

from flask import abort
from flask_login import current_user

from domain.permission import Permission


def permission_require(permission):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.can_do(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorator


def admin_required(f):
    return permission_require(Permission.ADMIN)(f)


def follow_required(f):
    return permission_require(Permission.FOLLOW)(f)


def moderator_required(f):
    return permission_require(Permission.MODERATE)(f)

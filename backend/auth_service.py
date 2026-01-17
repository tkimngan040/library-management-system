from functools import wraps
from flask import session, redirect, url_for, abort

from models import User
from security import verify_password


def authenticate(username: str, password: str):
    """
    Authenticate user by username and password.
    Returns User object if successful, otherwise None.
    """
    user = User.get_by_username(username)
    if not user:
        return None

    if verify_password(password, user.password):
        return user

    return None


def login_user(user):
    """
    Store user information in session after successful login.
    """
    session["user_id"] = user.user_id
    session["role"] = user.role


def logout_user():
    """
    Clear user session.
    """
    session.clear()


def get_current_user():
    """
    Get currently logged-in user from session.
    """
    user_id = session.get("user_id")
    if not user_id:
        return None

    return User.get_by_id(user_id)


def login_required(func):
    """
    Allow access only for authenticated users.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def role_required(required_role: str):
    """
    Allow access only for users with specific role.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))

            if session.get("role") != required_role:
                abort(403)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def guest_allowed(func):
    """
    Allow access for both guest and authenticated users.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

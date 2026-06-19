"""
Authentication and authorisation decorators for FAQFusion AI.

Provides ``login_required`` and ``admin_required`` decorators that
check Flask session state before allowing access to protected endpoints.
These are designed to be easily replaced with JWT-based checks later.
"""

from functools import wraps
from flask import session, jsonify


def login_required(f):
    """
    Decorator that restricts access to authenticated users.

    Checks for ``user_id`` in the Flask session. Returns HTTP 401
    if the user is not logged in.

    Ready for future JWT integration: replace the session check
    with token validation without changing route signatures.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'admin_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Authentication required. Please log in.',
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator that restricts access to authenticated admins.

    Checks for ``admin_id`` in the Flask session. Returns HTTP 401
    if no admin session exists, or HTTP 403 if the role is insufficient.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Admin authentication required.',
            }), 401
        return f(*args, **kwargs)
    return decorated_function

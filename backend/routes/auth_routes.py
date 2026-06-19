"""
Authentication routes for FAQFusion AI.

Endpoints:
    POST /register  — Create a new user account.
    POST /login     — Authenticate and start a session.
    POST /logout    — Destroy the current session.

All responses are JSON. Session-based authentication is used,
designed for easy migration to JWT in the future.
"""

import logging
from flask import Blueprint, request, jsonify, session

from database.db import db
from backend.models.user import User
from backend.models.admin import Admin
from backend.utils.validators import validate_registration, validate_login
from backend.utils.decorators import login_required

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


# ------------------------------------------------------------------
# POST /register
# ------------------------------------------------------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account.

    Request JSON:
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "secureP@ss1"
        }

    Returns:
        201: User created successfully.
        400: Validation error.
        409: Username or email already taken.
        500: Internal server error.
    """
    try:
        data = request.get_json(silent=True)
        error = validate_registration(data)
        if error:
            return jsonify({'success': False, 'message': error}), 400

        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']

        # Check for existing user
        if User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            return jsonify({
                'success': False,
                'message': 'Username or email already registered.',
            }), 409

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        logger.info('New user registered: %s (%s)', username, email)
        return jsonify({
            'success': True,
            'message': 'Registration successful.',
            'user': user.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.exception('Registration failed: %s', e)
        return jsonify({
            'success': False,
            'message': 'An internal error occurred during registration.',
        }), 500


# ------------------------------------------------------------------
# POST /login
# ------------------------------------------------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user or admin and start a session.

    The endpoint checks both User and Admin tables. If the email
    belongs to an admin, ``admin_id`` is stored in the session;
    otherwise ``user_id`` is stored.

    Request JSON:
        {
            "email": "john@example.com",
            "password": "secureP@ss1"
        }

    Returns:
        200: Login successful.
        400: Validation error.
        401: Invalid credentials.
        403: Account deactivated.
        500: Internal server error.
    """
    try:
        data = request.get_json(silent=True)
        error = validate_login(data)
        if error:
            return jsonify({'success': False, 'message': error}), 400

        email = data['email'].strip().lower()
        password = data['password']

        # Check admin table first
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if not admin.is_active:
                return jsonify({
                    'success': False,
                    'message': 'Account has been deactivated.',
                }), 403
            if admin.check_password(password):
                session.clear()
                session['admin_id'] = admin.id
                session['admin_username'] = admin.username
                session['role'] = admin.role
                session.permanent = True
                logger.info('Admin login: %s', admin.username)
                return jsonify({
                    'success': True,
                    'message': 'Admin login successful.',
                    'user': admin.to_dict(),
                    'is_admin': True,
                }), 200

        # Check regular user table
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                return jsonify({
                    'success': False,
                    'message': 'Account has been deactivated.',
                }), 403
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            logger.info('User login: %s', user.username)
            return jsonify({
                'success': True,
                'message': 'Login successful.',
                'user': user.to_dict(),
                'is_admin': False,
            }), 200

        return jsonify({
            'success': False,
            'message': 'Invalid email or password.',
        }), 401

    except Exception as e:
        logger.exception('Login failed: %s', e)
        return jsonify({
            'success': False,
            'message': 'An internal error occurred during login.',
        }), 500


# ------------------------------------------------------------------
# POST /logout
# ------------------------------------------------------------------

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Destroy the current user session.

    Returns:
        200: Logout successful.
    """
    username = session.get('username') or session.get('admin_username', 'unknown')
    session.clear()
    logger.info('User logged out: %s', username)
    return jsonify({
        'success': True,
        'message': 'Logged out successfully.',
    }), 200

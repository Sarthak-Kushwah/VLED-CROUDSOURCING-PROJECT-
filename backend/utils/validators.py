"""
Input validators for FAQFusion AI.

Pure functions that validate request payloads and return human-readable
error messages. Keeps validation logic out of route handlers.
"""

import re
from typing import Optional


def validate_registration(data: dict) -> Optional[str]:
    """
    Validate user registration payload.

    Required fields: username, email, password.

    Args:
        data: Parsed JSON request body.

    Returns:
        Error message string, or None if valid.
    """
    if not data:
        return 'Request body is required.'

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username:
        return 'Username is required.'
    if len(username) < 3 or len(username) > 80:
        return 'Username must be between 3 and 80 characters.'
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return 'Username may only contain letters, numbers, and underscores.'

    if not email:
        return 'Email is required.'
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return 'Invalid email format.'

    if not password:
        return 'Password is required.'
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'

    return None


def validate_login(data: dict) -> Optional[str]:
    """
    Validate login payload.

    Required fields: email, password.

    Args:
        data: Parsed JSON request body.

    Returns:
        Error message string, or None if valid.
    """
    if not data:
        return 'Request body is required.'

    if not data.get('email', '').strip():
        return 'Email is required.'
    if not data.get('password', ''):
        return 'Password is required.'

    return None


def validate_faq(data: dict) -> Optional[str]:
    """
    Validate FAQ creation / update payload.

    Required fields: question, answer.

    Args:
        data: Parsed JSON request body.

    Returns:
        Error message string, or None if valid.
    """
    if not data:
        return 'Request body is required.'

    if not data.get('question', '').strip():
        return 'Question text is required.'
    if not data.get('answer', '').strip():
        return 'Answer text is required.'

    return None


def validate_question(data: dict) -> Optional[str]:
    """
    Validate question submission payload.

    Required fields: question.

    Args:
        data: Parsed JSON request body.

    Returns:
        Error message string, or None if valid.
    """
    if not data:
        return 'Request body is required.'

    question = data.get('question', '').strip()
    if not question:
        return 'Question text is required.'
    if len(question) < 5:
        return 'Question must be at least 5 characters long.'

    return None

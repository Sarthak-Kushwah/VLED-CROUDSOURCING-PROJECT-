"""
Database initialization module for FAQFusion AI.

Provides the shared SQLAlchemy instance used across all models and
a helper function to initialize the database with the Flask application.
"""

from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance — imported by all model modules
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application.

    Binds the SQLAlchemy instance to the app, then creates all tables
    that don't yet exist based on registered models.

    Args:
        app: The Flask application instance.
    """
    db.init_app(app)
    with app.app_context():
        # Import all models so SQLAlchemy registers them before create_all()
        from backend.models import user, faq, question, admin  # noqa: F401
        db.create_all()

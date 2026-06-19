"""
Admin model for FAQFusion AI.

Represents admin users who can review pending questions, approve them,
provide answers, and manage the FAQ repository.
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db


class Admin(db.Model):
    """
    Administrative user with elevated privileges.

    Attributes:
        id:            Primary key.
        username:      Unique admin display name.
        email:         Unique admin email address.
        password_hash: Werkzeug-hashed password.
        role:          Admin role level (e.g., 'super_admin', 'moderator').
        is_active:     Whether the admin account is enabled.
        created_at:    Timestamp of account creation.
        updated_at:    Timestamp of last profile update.
    """

    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), default='moderator', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    faqs_created = db.relationship('FAQ', backref='creator', lazy='dynamic')

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def set_password(self, password: str) -> None:
        """Hash and store the admin's password."""
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha256'
        )

    def check_password(self, password: str) -> bool:
        """Verify a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-safe dictionary representation (no password)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<Admin {self.username!r} ({self.role})>'

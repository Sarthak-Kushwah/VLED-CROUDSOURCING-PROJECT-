"""
User model for FAQFusion AI.

Represents registered users who can submit questions and interact with
the FAQ system. Handles password hashing via Werkzeug utilities.
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db


class User(db.Model):
    """
    Application user capable of submitting questions.

    Attributes:
        id:         Primary key.
        username:   Unique display name.
        email:      Unique email address used for login.
        password_hash: Werkzeug-hashed password (never stored in plain text).
        is_active:  Soft-disable flag for account deactivation.
        created_at: Timestamp of account creation.
        updated_at: Timestamp of last profile update.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
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
    questions = db.relationship('Question', backref='author', lazy='dynamic')

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def set_password(self, password: str) -> None:
        """
        Hash and store the user's password.

        Uses Werkzeug's ``pbkdf2:sha256`` method by default.

        Args:
            password: The plain-text password to hash.
        """
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha256'
        )

    def check_password(self, password: str) -> bool:
        """
        Verify a plain-text password against the stored hash.

        Args:
            password: The plain-text password to verify.

        Returns:
            True if the password matches, False otherwise.
        """
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
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<User {self.username!r}>'

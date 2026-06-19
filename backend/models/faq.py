"""
FAQ model for FAQFusion AI.

Represents curated FAQ entries in the knowledge repository. Each FAQ
contains a canonical question, its answer, and an optional category
for organizational purposes.
"""

from datetime import datetime, timezone
from database.db import db


class FAQ(db.Model):
    """
    A curated frequently-asked question with its answer.

    Attributes:
        id:         Primary key.
        question:   The canonical question text.
        answer:     The approved answer text.
        category:   Optional category label for grouping FAQs.
        is_active:  Whether this FAQ is publicly visible.
        created_by: ID of the admin/user who created this FAQ.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_by = db.Column(
        db.Integer, db.ForeignKey('admins.id'), nullable=True
    )
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-safe dictionary representation."""
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<FAQ {self.id}: {self.question[:50]!r}>'

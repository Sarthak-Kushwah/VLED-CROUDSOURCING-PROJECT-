"""
Question model for FAQFusion AI.

Represents user-submitted questions. Each question progresses through
statuses: pending → answered | approved | rejected.
When the AI engine finds a match, it auto-answers; otherwise the question
stays pending for admin review.
"""

from datetime import datetime, timezone
from database.db import db


class QuestionStatus:
    """Enumeration of valid question statuses."""
    PENDING = 'pending'
    ANSWERED = 'answered'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    ALL = {PENDING, ANSWERED, APPROVED, REJECTED}


class Question(db.Model):
    """
    A question submitted by an authenticated user.

    Attributes:
        id:               Primary key.
        question_text:    The raw question submitted by the user.
        answer_text:      AI-generated or admin-provided answer (nullable).
        status:           Current lifecycle status (see ``QuestionStatus``).
        similarity_score: Cosine similarity to the matched FAQ (if any).
        matched_faq_id:   FK to the FAQ that was matched (nullable).
        user_id:          FK to the submitting user.
        created_at:       Timestamp of submission.
        updated_at:       Timestamp of last status change.
    """

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), default=QuestionStatus.PENDING, nullable=False, index=True
    )
    similarity_score = db.Column(db.Float, nullable=True)
    matched_faq_id = db.Column(
        db.Integer, db.ForeignKey('faqs.id'), nullable=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
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

    # Relationships
    matched_faq = db.relationship('FAQ', backref='matched_questions', lazy='joined')

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-safe dictionary representation."""
        return {
            'id': self.id,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'status': self.status,
            'similarity_score': self.similarity_score,
            'matched_faq_id': self.matched_faq_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<Question {self.id} [{self.status}]>'

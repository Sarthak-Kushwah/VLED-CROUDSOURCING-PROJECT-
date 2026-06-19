"""
Question submission routes for FAQFusion AI.

Endpoints:
    POST /ask-question — Submit a question (authenticated users only).

The route feeds the question through the AI Similarity Engine.
If a close enough FAQ match is found, the answer is returned
immediately; otherwise the question is saved as "pending" for
admin review.
"""

import logging
from flask import Blueprint, request, jsonify, session

from database.db import db
from backend.models.question import Question, QuestionStatus
from backend.utils.validators import validate_question
from backend.utils.decorators import login_required
from backend.services.similarity_engine import similarity_engine

logger = logging.getLogger(__name__)

question_bp = Blueprint('question', __name__)


# ------------------------------------------------------------------
# POST /ask-question
# ------------------------------------------------------------------

@question_bp.route('/ask-question', methods=['POST'])
@login_required
def ask_question():
    """
    Submit a question and receive an AI-powered answer (if available).

    Workflow:
        1. Validate the request payload.
        2. Run the question through the Similarity Engine.
        3a. If a match is found (score ≥ threshold):
            - Store the question with status ``answered``.
            - Return the matched FAQ answer immediately.
        3b. If no match:
            - Store the question with status ``pending``.
            - Notify the user that an admin will review it.

    Request JSON:
        {
            "question": "How do I reset my password?"
        }

    Returns:
        200: Answer found — returns the matched FAQ answer.
        202: No match — question saved for admin review.
        400: Validation error.
        500: Internal server error.
    """
    try:
        data = request.get_json(silent=True)
        error = validate_question(data)
        if error:
            return jsonify({'success': False, 'message': error}), 400

        question_text = data['question'].strip()
        user_id = session['user_id']

        # Run similarity matching
        match_result = similarity_engine.find_best_match(question_text)

        if match_result['matched']:
            # Auto-answer: save with status 'answered'
            question = Question(
                question_text=question_text,
                answer_text=match_result['faq']['answer'],
                status=QuestionStatus.ANSWERED,
                similarity_score=match_result['score'],
                matched_faq_id=match_result['faq']['id'],
                user_id=user_id,
            )
            db.session.add(question)
            db.session.commit()

            logger.info(
                'Question auto-answered (id=%d, score=%.4f, faq=%d)',
                question.id, match_result['score'], match_result['faq']['id'],
            )
            return jsonify({
                'success': True,
                'message': 'Answer found!',
                'auto_answered': True,
                'question': question.to_dict(),
                'matched_faq': match_result['faq'],
                'similarity_score': match_result['score'],
            }), 200

        else:
            # No match: save as pending
            question = Question(
                question_text=question_text,
                status=QuestionStatus.PENDING,
                similarity_score=match_result['score'],
                user_id=user_id,
            )
            db.session.add(question)
            db.session.commit()

            logger.info(
                'Question saved as pending (id=%d, best_score=%s)',
                question.id, match_result['score'],
            )
            return jsonify({
                'success': True,
                'message': (
                    'No matching answer found. Your question has been '
                    'submitted for review by an admin.'
                ),
                'auto_answered': False,
                'question': question.to_dict(),
                'similarity_score': match_result['score'],
            }), 202

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to process question: %s', e)
        return jsonify({
            'success': False,
            'message': 'An internal error occurred while processing your question.',
        }), 500

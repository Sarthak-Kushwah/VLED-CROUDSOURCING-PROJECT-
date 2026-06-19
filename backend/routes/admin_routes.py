"""
Admin management routes for FAQFusion AI.

Endpoints:
    GET  /pending-questions        — List all pending questions.
    POST /approve-question/<id>    — Approve a question and provide an answer.

Admin endpoints are protected by the ``admin_required`` decorator.
"""

import logging
from flask import Blueprint, request, jsonify, session

from database.db import db
from backend.models.question import Question, QuestionStatus
from backend.models.faq import FAQ
from backend.utils.decorators import admin_required

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)


# ------------------------------------------------------------------
# GET /pending-questions
# ------------------------------------------------------------------

@admin_bp.route('/pending-questions', methods=['GET'])
@admin_required
def pending_questions():
    """
    List all questions with status ``pending``.

    Query Parameters:
        page     (int): Page number (default 1).
        per_page (int): Results per page (default 20, max 100).

    Returns:
        200: Paginated list of pending questions.
        500: Internal server error.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)

        pagination = (
            Question.query
            .filter_by(status=QuestionStatus.PENDING)
            .order_by(Question.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return jsonify({
            'success': True,
            'questions': [q.to_dict() for q in pagination.items],
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
            },
        }), 200

    except Exception as e:
        logger.exception('Failed to list pending questions: %s', e)
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve pending questions.',
        }), 500


# ------------------------------------------------------------------
# POST /approve-question/<id>
# ------------------------------------------------------------------

@admin_bp.route('/approve-question/<int:question_id>', methods=['POST'])
@admin_required
def approve_question(question_id):
    """
    Approve a pending question and optionally convert it into a FAQ.

    Workflow:
        1. Fetch the pending question by ID.
        2. Validate that an answer is provided.
        3. Update the question status to ``approved`` and save the answer.
        4. If ``add_to_faq`` is True, create a new FAQ entry from the
           approved question–answer pair.

    Request JSON:
        {
            "answer": "Here is the answer to your question.",
            "add_to_faq": true,      // optional, default false
            "category": "General"    // optional, used only if add_to_faq is true
        }

    Args:
        question_id: The primary key of the question to approve.

    Returns:
        200: Question approved (and optionally added to FAQs).
        400: Validation error.
        404: Question not found or not in pending status.
        500: Internal server error.
    """
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({
                'success': False,
                'message': f'Question with id {question_id} not found.',
            }), 404

        if question.status != QuestionStatus.PENDING:
            return jsonify({
                'success': False,
                'message': (
                    f'Question is not pending. Current status: {question.status}.'
                ),
            }), 400

        data = request.get_json(silent=True)
        if not data or not data.get('answer', '').strip():
            return jsonify({
                'success': False,
                'message': 'An answer is required to approve the question.',
            }), 400

        answer_text = data['answer'].strip()
        add_to_faq = data.get('add_to_faq', False)

        # Update question
        question.answer_text = answer_text
        question.status = QuestionStatus.APPROVED

        response_data = {
            'success': True,
            'message': 'Question approved successfully.',
            'question': question.to_dict(),
        }

        # Optionally convert to FAQ
        if add_to_faq:
            faq = FAQ(
                question=question.question_text,
                answer=answer_text,
                category=data.get('category', '').strip() or None,
                created_by=session.get('admin_id'),
            )
            db.session.add(faq)
            db.session.flush()  # Get the faq.id before commit
            question.matched_faq_id = faq.id
            response_data['message'] = (
                'Question approved and added to FAQ repository.'
            )
            response_data['faq'] = faq.to_dict()

        db.session.commit()

        logger.info(
            'Question %d approved by admin %d (add_to_faq=%s)',
            question_id, session.get('admin_id'), add_to_faq,
        )
        return jsonify(response_data), 200

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to approve question %d: %s', question_id, e)
        return jsonify({
            'success': False,
            'message': 'Failed to approve question.',
        }), 500


# ------------------------------------------------------------------
# POST /reject-question/<id>
# ------------------------------------------------------------------

@admin_bp.route('/reject-question/<int:question_id>', methods=['POST'])
@admin_required
def reject_question(question_id):
    """
    Reject a pending question.

    Request JSON (optional):
        {
            "reason": "This question is outside our scope."
        }

    Args:
        question_id: The primary key of the question to reject.

    Returns:
        200: Question rejected.
        404: Question not found or not pending.
        500: Internal server error.
    """
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({
                'success': False,
                'message': f'Question with id {question_id} not found.',
            }), 404

        if question.status != QuestionStatus.PENDING:
            return jsonify({
                'success': False,
                'message': (
                    f'Question is not pending. Current status: {question.status}.'
                ),
            }), 400

        data = request.get_json(silent=True) or {}
        reason = data.get('reason', '').strip()

        question.status = QuestionStatus.REJECTED
        if reason:
            question.answer_text = f'[Rejected] {reason}'

        db.session.commit()

        logger.info('Question %d rejected by admin %d', question_id, session.get('admin_id'))
        return jsonify({
            'success': True,
            'message': 'Question rejected.',
            'question': question.to_dict(),
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to reject question %d: %s', question_id, e)
        return jsonify({
            'success': False,
            'message': 'Failed to reject question.',
        }), 500

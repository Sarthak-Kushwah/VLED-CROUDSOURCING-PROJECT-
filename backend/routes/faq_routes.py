"""
FAQ management routes for FAQFusion AI.

Endpoints:
    GET    /faqs              — List all active FAQs (with search & pagination).
    GET    /faq/<id>          — Retrieve a single FAQ by ID.
    POST   /faq/add           — Create a new FAQ (admin only).
    PUT    /faq/update/<id>   — Update an existing FAQ (admin only).
    DELETE /faq/delete/<id>   — Soft-delete a FAQ (admin only).

All responses are JSON.
"""

import logging
from flask import Blueprint, request, jsonify, session, current_app

from database.db import db
from backend.models.faq import FAQ
from backend.utils.validators import validate_faq
from backend.utils.decorators import admin_required

logger = logging.getLogger(__name__)

faq_bp = Blueprint('faq', __name__)


# ------------------------------------------------------------------
# GET /faqs
# ------------------------------------------------------------------

@faq_bp.route('/faqs', methods=['GET'])
def list_faqs():
    """
    List all active FAQs with optional search and pagination.

    Query Parameters:
        search   (str):  Full-text search across question and answer.
        category (str):  Filter by category.
        page     (int):  Page number (default 1).
        per_page (int):  Results per page (default 20, max 100).

    Returns:
        200: Paginated list of FAQs.
        500: Internal server error.
    """
    try:
        search = request.args.get('search', '', type=str).strip()
        category = request.args.get('category', '', type=str).strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(
            request.args.get('per_page', current_app.config.get('DEFAULT_PAGE_SIZE', 20), type=int),
            current_app.config.get('MAX_PAGE_SIZE', 100),
        )

        query = FAQ.query.filter_by(is_active=True)

        # Apply filters
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                (FAQ.question.ilike(search_pattern)) |
                (FAQ.answer.ilike(search_pattern))
            )
        if category:
            query = query.filter_by(category=category)

        query = query.order_by(FAQ.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'success': True,
            'faqs': [faq.to_dict() for faq in pagination.items],
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
        logger.exception('Failed to list FAQs: %s', e)
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve FAQs.',
        }), 500


# ------------------------------------------------------------------
# GET /faq/<id>
# ------------------------------------------------------------------

@faq_bp.route('/faq/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    """
    Retrieve a single FAQ by its ID.

    Args:
        faq_id: The primary key of the FAQ.

    Returns:
        200: FAQ details.
        404: FAQ not found.
        500: Internal server error.
    """
    try:
        faq = FAQ.query.filter_by(id=faq_id, is_active=True).first()
        if not faq:
            return jsonify({
                'success': False,
                'message': f'FAQ with id {faq_id} not found.',
            }), 404

        return jsonify({
            'success': True,
            'faq': faq.to_dict(),
        }), 200

    except Exception as e:
        logger.exception('Failed to retrieve FAQ %d: %s', faq_id, e)
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve FAQ.',
        }), 500


# ------------------------------------------------------------------
# POST /faq/add
# ------------------------------------------------------------------

@faq_bp.route('/faq/add', methods=['POST'])
@admin_required
def add_faq():
    """
    Create a new FAQ entry (admin only).

    Request JSON:
        {
            "question": "How do I reset my password?",
            "answer": "Click Forgot Password on the login page.",
            "category": "Account"   // optional
        }

    Returns:
        201: FAQ created.
        400: Validation error.
        500: Internal server error.
    """
    try:
        data = request.get_json(silent=True)
        error = validate_faq(data)
        if error:
            return jsonify({'success': False, 'message': error}), 400

        faq = FAQ(
            question=data['question'].strip(),
            answer=data['answer'].strip(),
            category=data.get('category', '').strip() or None,
            created_by=session.get('admin_id'),
        )
        db.session.add(faq)
        db.session.commit()

        logger.info('FAQ created (id=%d) by admin %d', faq.id, session.get('admin_id'))
        return jsonify({
            'success': True,
            'message': 'FAQ created successfully.',
            'faq': faq.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to create FAQ: %s', e)
        return jsonify({
            'success': False,
            'message': 'Failed to create FAQ.',
        }), 500


# ------------------------------------------------------------------
# PUT /faq/update/<id>
# ------------------------------------------------------------------

@faq_bp.route('/faq/update/<int:faq_id>', methods=['PUT'])
@admin_required
def update_faq(faq_id):
    """
    Update an existing FAQ (admin only).

    Request JSON (all fields optional):
        {
            "question": "Updated question?",
            "answer": "Updated answer.",
            "category": "General",
            "is_active": true
        }

    Args:
        faq_id: The primary key of the FAQ to update.

    Returns:
        200: FAQ updated.
        400: Validation error.
        404: FAQ not found.
        500: Internal server error.
    """
    try:
        faq = FAQ.query.get(faq_id)
        if not faq:
            return jsonify({
                'success': False,
                'message': f'FAQ with id {faq_id} not found.',
            }), 404

        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required.',
            }), 400

        # Apply partial updates
        if 'question' in data:
            question = data['question'].strip()
            if not question:
                return jsonify({
                    'success': False,
                    'message': 'Question text cannot be empty.',
                }), 400
            faq.question = question

        if 'answer' in data:
            answer = data['answer'].strip()
            if not answer:
                return jsonify({
                    'success': False,
                    'message': 'Answer text cannot be empty.',
                }), 400
            faq.answer = answer

        if 'category' in data:
            faq.category = data['category'].strip() or None

        if 'is_active' in data:
            faq.is_active = bool(data['is_active'])

        db.session.commit()

        logger.info('FAQ updated (id=%d) by admin %d', faq.id, session.get('admin_id'))
        return jsonify({
            'success': True,
            'message': 'FAQ updated successfully.',
            'faq': faq.to_dict(),
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to update FAQ %d: %s', faq_id, e)
        return jsonify({
            'success': False,
            'message': 'Failed to update FAQ.',
        }), 500


# ------------------------------------------------------------------
# DELETE /faq/delete/<id>
# ------------------------------------------------------------------

@faq_bp.route('/faq/delete/<int:faq_id>', methods=['DELETE'])
@admin_required
def delete_faq(faq_id):
    """
    Soft-delete a FAQ by marking it inactive (admin only).

    This does not physically remove the record; it sets ``is_active``
    to False so the FAQ no longer appears in public listings.

    Args:
        faq_id: The primary key of the FAQ to delete.

    Returns:
        200: FAQ deleted.
        404: FAQ not found.
        500: Internal server error.
    """
    try:
        faq = FAQ.query.get(faq_id)
        if not faq:
            return jsonify({
                'success': False,
                'message': f'FAQ with id {faq_id} not found.',
            }), 404

        faq.is_active = False
        db.session.commit()

        logger.info('FAQ soft-deleted (id=%d) by admin %d', faq.id, session.get('admin_id'))
        return jsonify({
            'success': True,
            'message': 'FAQ deleted successfully.',
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.exception('Failed to delete FAQ %d: %s', faq_id, e)
        return jsonify({
            'success': False,
            'message': 'Failed to delete FAQ.',
        }), 500

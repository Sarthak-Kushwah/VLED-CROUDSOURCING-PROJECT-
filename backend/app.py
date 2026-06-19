"""
FAQFusion AI — Application Entry Point.

Provides the ``create_app()`` factory function that wires together
configuration, database, blueprints, error handlers, and the AI
similarity engine.

Usage (development):
    $ flask --app backend.app run --debug

Usage (production):
    $ gunicorn "backend.app:create_app()"
"""

import logging
import os
import sys

from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import config_by_name
from database.db import db, init_db
from backend.services.similarity_engine import similarity_engine


def create_app(config_name: str | None = None) -> Flask:
    """
    Application factory for FAQFusion AI.

    Args:
        config_name: One of ``'development'``, ``'testing'``, or
                     ``'production'``. Defaults to the ``FLASK_ENV``
                     environment variable, or ``'development'``.

    Returns:
        A fully configured Flask application instance.
    """
    # ------------------------------------------------------------------
    # 1. Initialise Flask
    # ------------------------------------------------------------------
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))

    # ------------------------------------------------------------------
    # 2. Logging
    # ------------------------------------------------------------------
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        stream=sys.stdout,
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting FAQFusion AI in "%s" mode …', config_name)

    # ------------------------------------------------------------------
    # 3. Extensions
    # ------------------------------------------------------------------
    CORS(app, supports_credentials=True)

    # ------------------------------------------------------------------
    # 4. Database
    # ------------------------------------------------------------------
    init_db(app)

    # ------------------------------------------------------------------
    # 5. AI Similarity Engine (lazy load in non-test environments)
    # ------------------------------------------------------------------
    if not app.config.get('TESTING'):
        with app.app_context():
            similarity_engine.model_name = app.config['TRANSFORMER_MODEL']
            similarity_engine.threshold = app.config['SIMILARITY_THRESHOLD']
            try:
                similarity_engine.load_model()
            except Exception as e:
                logger.warning(
                    'Failed to pre-load SentenceTransformer model: %s. '
                    'The model will be loaded on first request.', e,
                )

    # ------------------------------------------------------------------
    # 6. Register Blueprints
    # ------------------------------------------------------------------
    from backend.routes.auth_routes import auth_bp
    from backend.routes.faq_routes import faq_bp
    from backend.routes.question_routes import question_bp
    from backend.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(faq_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(admin_bp)

    # ------------------------------------------------------------------
    # 7. Global Error Handlers
    # ------------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request.',
            'error': str(error),
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found.',
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method not allowed.',
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'An internal server error occurred.',
        }), 500

    # ------------------------------------------------------------------
    # 8. Health check
    # ------------------------------------------------------------------
    @app.route('/health', methods=['GET'])
    def health_check():
        """Simple health-check endpoint for load balancers / monitoring."""
        return jsonify({
            'success': True,
            'message': 'FAQFusion AI is running.',
            'status': 'healthy',
        }), 200

    logger.info('FAQFusion AI application ready.')
    return app


# ------------------------------------------------------------------
# Direct invocation (python -m backend.app)
# ------------------------------------------------------------------
if __name__ == '__main__':
    application = create_app()
    application.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=True,
    )

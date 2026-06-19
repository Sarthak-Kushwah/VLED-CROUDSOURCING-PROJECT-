"""
AI Similarity Engine for FAQFusion AI.

Uses Sentence Transformers (``all-MiniLM-L6-v2``) to encode questions
and scikit-learn's ``cosine_similarity`` to find the closest FAQ match
in the knowledge repository.

The engine is designed as a singleton: the transformer model is loaded
once and reused across requests to avoid repeated cold-start latency.
"""

import logging
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.models.faq import FAQ

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """
    NLP-powered similarity matcher for FAQ lookups.

    Lifecycle:
        1. ``load_model()`` — loads the transformer (call once at startup).
        2. ``find_best_match(question)`` — compares against all active FAQs.

    Thread Safety:
        SentenceTransformer.encode() is thread-safe for inference, so
        this engine can be safely used from multiple Flask request threads.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2',
                 threshold: float = 0.75):
        """
        Args:
            model_name: Hugging Face model identifier for the sentence
                        transformer. Defaults to ``all-MiniLM-L6-v2``.
            threshold:  Minimum cosine similarity to consider a match.
        """
        self.model_name = model_name
        self.threshold = threshold
        self._model: Optional[SentenceTransformer] = None

    # ------------------------------------------------------------------
    # Model management
    # ------------------------------------------------------------------

    def load_model(self) -> None:
        """
        Load the SentenceTransformer model into memory.

        Call this once during application startup (inside app context).
        Subsequent calls are no-ops.
        """
        if self._model is not None:
            logger.debug('SentenceTransformer model already loaded; skipping.')
            return

        logger.info('Loading SentenceTransformer model: %s …', self.model_name)
        self._model = SentenceTransformer(self.model_name)
        logger.info('Model loaded successfully.')

    @property
    def model(self) -> SentenceTransformer:
        """Return the loaded model, raising if not yet initialised."""
        if self._model is None:
            raise RuntimeError(
                'SimilarityEngine model not loaded. '
                'Call load_model() during app startup.'
            )
        return self._model

    # ------------------------------------------------------------------
    # Core matching logic
    # ------------------------------------------------------------------

    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode a single text string into a dense vector embedding.

        Args:
            text: The text to encode.

        Returns:
            A 1-D numpy array representing the embedding.
        """
        return self.model.encode([text], show_progress_bar=False)[0]

    def find_best_match(self, question_text: str) -> dict:
        """
        Search the FAQ repository for the closest semantic match.

        Algorithm:
            1. Fetch all active FAQs from the database.
            2. Encode the user question and all FAQ questions.
            3. Compute cosine similarity between the user question
               embedding and every FAQ embedding.
            4. Select the FAQ with the highest similarity score.
            5. If the score ≥ ``self.threshold``, return the match.

        Args:
            question_text: The user-submitted question.

        Returns:
            A dict with keys:
                - ``matched``  (bool): Whether a match was found.
                - ``faq``      (dict | None): The matched FAQ's ``to_dict()``.
                - ``score``    (float | None): The similarity score.
                - ``threshold``(float): The current threshold value.
        """
        # 1. Retrieve active FAQs
        faqs = FAQ.query.filter_by(is_active=True).all()
        if not faqs:
            logger.info('No active FAQs in the repository.')
            return {
                'matched': False,
                'faq': None,
                'score': None,
                'threshold': self.threshold,
            }

        # 2. Encode
        faq_questions = [faq.question for faq in faqs]
        user_embedding = self.encode_text(question_text).reshape(1, -1)
        faq_embeddings = self.model.encode(
            faq_questions, show_progress_bar=False
        )

        # 3. Cosine similarity
        similarities = cosine_similarity(user_embedding, faq_embeddings)[0]

        # 4. Best match
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        logger.info(
            'Best similarity score: %.4f (threshold: %.4f)',
            best_score, self.threshold,
        )

        # 5. Threshold check
        if best_score >= self.threshold:
            matched_faq = faqs[best_idx]
            return {
                'matched': True,
                'faq': matched_faq.to_dict(),
                'score': round(best_score, 4),
                'threshold': self.threshold,
            }

        return {
            'matched': False,
            'faq': None,
            'score': round(best_score, 4),
            'threshold': self.threshold,
        }

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def set_threshold(self, threshold: float) -> None:
        """
        Update the similarity threshold at runtime.

        Args:
            threshold: New threshold value (0.0 – 1.0).

        Raises:
            ValueError: If the threshold is outside the valid range.
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError('Threshold must be between 0.0 and 1.0.')
        self.threshold = threshold
        logger.info('Similarity threshold updated to %.4f', threshold)


# Module-level singleton — initialised by the app factory
similarity_engine = SimilarityEngine()

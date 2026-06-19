"""
Configuration module for FAQFusion AI.

Loads environment variables and provides configuration classes
for different deployment environments (development, testing, production).
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


class Config:
    """Base configuration class with shared settings."""

    # Flask core settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-not-for-production')
    
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:password@localhost:3306/faqfusion_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=int(os.getenv('SESSION_LIFETIME_MINUTES', 60))
    )

    # AI Similarity Engine settings
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.75))
    TRANSFORMER_MODEL = os.getenv('TRANSFORMER_MODEL', 'all-MiniLM-L6-v2')

    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False


# Configuration map for easy access
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

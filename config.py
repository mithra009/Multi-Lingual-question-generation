"""
Configuration settings for the Multi-Lingual Question Generation application.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Model settings - Using a more stable model
    QUESTION_GENERATOR_MODEL = "google/flan-t5-small"  # More stable alternative
    MAX_QUESTIONS_PER_CHUNK = 3
    DEFAULT_TOTAL_QUESTIONS = 20
    DEFAULT_TOP_N_CHUNKS = 5
    CHUNK_SIZE = 1000
    
    # Translation settings
    TRANSLATION_TIMEOUT = 10  # seconds
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'english': 'en',
        'hindi': 'hi', 
        'sanskrit': 'sa'
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 
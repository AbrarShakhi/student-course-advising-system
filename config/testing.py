import os
import tempfile
from config.base import BaseConfig

class TestingConfig(BaseConfig):
    """Testing configuration"""
    
    DEBUG = False
    TESTING = True
    
    # Database Configuration - Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Use a temporary directory for uploads during testing
    UPLOAD_FOLDER = tempfile.mkdtemp()
    
    # Testing-specific settings
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    # Disable logging during tests
    LOG_LEVEL = 'ERROR'
    
    # Use a simple secret key for testing
    SECRET_KEY = 'test-secret-key'
    
    @staticmethod
    def init_app(app):
        """Initialize testing-specific settings"""
        BaseConfig.init_app(app) 
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration class with common settings"""

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Flask-Login Configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    REMEMBER_COOKIE_SECURE = False  # Set to True in production with HTTPS
    REMEMBER_COOKIE_HTTPONLY = True

    # Flask-Admin Configuration
    FLASK_ADMIN_SWATCH = "cerulean"

    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}

    # Email Configuration for yagmail
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    # Application Configuration
    APP_NAME = "Student Course Advising System"
    APP_VERSION = "1.0.0"
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")

    # Pagination
    ITEMS_PER_PAGE = 20

    # Security
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

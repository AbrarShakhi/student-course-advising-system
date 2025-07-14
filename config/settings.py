"""
Application settings and environment variable management
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Environment
ENVIRONMENT = os.environ.get("FLASK_ENV", "development")

# Database settings
DATABASE_URL = os.environ.get("DATABASE_URL")

# Security
SECRET_KEY = os.environ.get("SECRET_KEY")

# Email settings for yagmail
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Admin settings
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# File upload settings
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16MB

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE = os.environ.get("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

# Application settings
APP_NAME = "Student Course Advising System"
APP_VERSION = "1.0.0"
DEBUG = ENVIRONMENT == "development"
TESTING = ENVIRONMENT == "testing"

# Pagination
ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 20))

# Security settings
SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
REMEMBER_COOKIE_SECURE = ENVIRONMENT == "production"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Flask-Admin settings
FLASK_ADMIN_SWATCH = "cerulean"

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {
    "image": {"png", "jpg", "jpeg", "gif"},
    "document": {"pdf", "doc", "docx", "txt"},
    "all": {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"},
}

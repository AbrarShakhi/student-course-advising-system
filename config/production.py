import os
from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    TESTING = False

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required for production")

    # Security Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required for production")

    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FILE = os.environ.get("LOG_FILE") or "/var/log/student-advising/app.log"

    # Production-specific settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Security headers
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Email Configuration
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # File upload settings
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max file size

    @staticmethod
    def init_app(app):
        """Initialize production-specific settings"""
        BaseConfig.init_app(app)

        # Production logging setup
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug and not app.testing:
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(app.config["LOG_FILE"])
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Set up file logging
            file_handler = RotatingFileHandler(
                app.config["LOG_FILE"], maxBytes=10240000, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info("Student Course Advising System startup")

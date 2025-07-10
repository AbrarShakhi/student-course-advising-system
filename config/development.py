import os
from config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True
    TESTING = False

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "instance", "dev.db"
    )

    # Logging Configuration
    LOG_LEVEL = "DEBUG"
    LOG_FILE = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "logs", "dev.log"
    )

    # Development-specific settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Debug toolbar (if installed)
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Development email settings
    MAIL_DEBUG = True

    @staticmethod
    def init_app(app):
        """Initialize development-specific settings"""
        BaseConfig.init_app(app)

        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(app.config["LOG_FILE"])
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

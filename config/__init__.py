import os

from config.base import BaseConfig
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])

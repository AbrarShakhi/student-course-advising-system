from flask import Flask
from flask_login import LoginManager

from config import get_config
from app.admin import init_admin
from app.models.admin_user import AdminUser
from app.admin.views import admin_auth
from app.core.db import db
from app.core.jwt import init_jwt  # <-- Import JWT init from core
from app.api.auth.routes import auth_bp  # <-- Only import blueprint


def create_app():
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    init_admin(app, db)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "admin_auth.admin_login"

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # Register admin login/logout blueprint
    app.register_blueprint(admin_auth)

    # Register API auth blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Initialize JWT
    init_jwt(app)

    return app

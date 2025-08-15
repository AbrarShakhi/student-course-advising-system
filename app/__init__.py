from typing import Any
from flask import Flask
from flask_login import LoginManager
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from config import get_config

from app.admin import register_crud_blueprints
from app.models.admin_user import AdminUser
from app.core.db import db
from app.core.jwt import init_jwt
from app.api.routes import api_bp
from app.admin.admin_routes import admin_api_bp


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    config = get_config()
    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    register_crud_blueprints(app)

    login_manager: LoginManager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = "admin_auth.admin_login"

    @login_manager.user_loader
    def load_user(user_id) -> Any | None:
        return AdminUser.query.get(int(user_id))

    app.register_blueprint(api_bp, url_prefix="/api")

    init_jwt(app)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    return app

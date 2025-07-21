from typing import Any
from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from config import get_config

from app.admin import init_admin
from app.models.admin_user import AdminUser
from app.core.db import db
from app.core.jwt import init_jwt
from app.api.routes import api_bp, login


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    config = get_config()
    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    init_admin(app, db)

    limiter: Limiter = Limiter(
        get_remote_address, app=app, default_limits=["400 per day", "70 per hour"]
    )

    login_manager: LoginManager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = "admin_auth.admin_login"

    @login_manager.user_loader
    def load_user(user_id) -> Any | None:
        return AdminUser.query.get(int(user_id))

    app.register_blueprint(api_bp, url_prefix="/api")

    init_jwt(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app

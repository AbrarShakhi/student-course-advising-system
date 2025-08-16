from flask import Flask
from flask_cors import CORS

from config import get_config

from app.admin import register_crud_blueprints
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

    app.register_blueprint(api_bp, url_prefix="/api")
    register_crud_blueprints(app)

    init_jwt(app)
    CORS(
        app,
        origins=["*"],
        supports_credentials=True,
        resources={r"/*": {"origins": "*"}},
    )

    return app

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

# In-memory token blacklist for demonstration (use persistent storage in production)
jwt_blacklist = set()


def init_jwt(app:Flask) -> JWTManager:
    app.config.setdefault(
        "JWT_SECRET_KEY", "super-secret"
    )  # Change this in production!
    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(hours=1))
    app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # Set True in production with HTTPS
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Enable in production if needed
    jwt = JWTManager(app)

    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
        jti = jwt_payload["jti"]
        return jti in jwt_blacklist

    return jwt

from flask import Blueprint, current_app, jsonify, request
from app.core.jwt import jwt_blacklist
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt,
)

from app.models.admin_user import AdminUser
from app.admin.admin_controllers.admin_user import (
    admin_login_controller,
    admin_logout_controller,
)
from app.core.responses import internal_server_error


admin_api_bp = Blueprint("admin", __name__)


@admin_api_bp.route("/login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        return admin_login_controller(username, password)
    except Exception as e:
        current_app.logger.error(f"Admin login failed: {str(e)}")
        return internal_server_error()


@admin_api_bp.route("/logout", methods=["POST"])
@jwt_required()
def admin_logout():
    try:
        jti = get_jwt()["jti"]
        return admin_logout_controller(jti, jwt_blacklist)
    except:
        return internal_server_error()

# This is the new endpoint to check if the user is authenticated.
@admin_api_bp.route("/check-auth", methods=["GET"])
@jwt_required()
def admin_check_auth():
    """
    Checks if a valid JWT is present.
    The @jwt_required() decorator handles the authentication check.
    If the token is valid, it returns a 200 OK.
    If the token is invalid, it automatically returns a 401 Unauthorized,
    which the frontend's PrivateGuard will catch.
    """
    return jsonify({"message": "Token is valid", "user": get_jwt_identity()}), 200
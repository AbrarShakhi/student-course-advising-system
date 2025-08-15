from flask import Response, current_app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity

from app.core.responses import login_success, logout_success
from app.models.admin_user import AdminUser


def admin_login_controller(username, password) -> tuple[Response, int] | Response:
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Find the admin user by username
    admin_user = AdminUser.query.filter_by(username=username).first()

    if not admin_user or not admin_user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

    if not admin_user.is_active_user:
        return jsonify({"msg": "User is inactive"}), 403

    access_token = create_access_token(identity=username)
    current_app.logger.info(
        f"[AUDIT] Successful login for admin username={username} from {request.remote_addr}"
    )
    response = login_success(access_token=access_token)
    response.set_cookie(
        "access_token_cookie",
        access_token,
        httponly=True,
        secure=False,  # Set True in production
        samesite="Lax",
    )
    return response


def admin_logout_controller(
    jti, jwt_blacklist, res=None
) -> tuple[Response, int] | Response:
    jwt_blacklist.add(jti)
    username = None
    try:
        username = get_jwt_identity()
    except Exception:
        pass
    current_app.logger.info(
        f"[AUDIT] Logout for student_id={username} from {request.remote_addr}"
    )
    if not res:
        res = jsonify({"message": "Logout successful."}), 200
    return logout_success(res)

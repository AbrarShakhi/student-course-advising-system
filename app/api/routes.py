from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from app.core.responses import internal_server_error
from app.core.jwt import jwt_blacklist
from app.api.controllers.auth import (
    login_controller,
    logout_controller,
    activate_controller,
)


api_bp = Blueprint("api", __name__)


@api_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        raw_password = data.get("password")
        return login_controller(student_id, raw_password)
    except:
        return internal_server_error()


@api_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        return logout_controller(jti, jwt_blacklist)
    except:
        return internal_server_error()


@api_bp.route("/activate", methods=["POST"])
def activate():
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        raw_otp = data.get("otp")
        raw_password = data.get("password")
        return activate_controller(student_id, raw_otp, raw_password)
    except:
        return internal_server_error()


@api_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    pass


@api_bp.route("/send-otp", methods=["PATCH"])
def send_otp():
    pass


@api_bp.route("/home", methods=["GET"])
def home():
    pass


@api_bp.route("/change-password", methods=["PATCH"])
def change_password():
    pass

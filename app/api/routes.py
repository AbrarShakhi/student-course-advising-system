from flask import Blueprint, current_app, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from app.core.responses import internal_server_error
from app.api.controllers.update import (
    change_password_controller,
    forget_password_controller,
)
from app.core.jwt import jwt_blacklist
from app.api.controllers.auth import (
    login_controller,
    logout_controller,
    activate_controller,
    welcome_controller,
    relog_controller,
)
from app.api.controllers.otp import send_otp_controller
from app.api.controllers.basics import (
    list_semesters_controller,
    university_info_controller,
    class_schedule_controller,
)
from app.models import Student


api_bp = Blueprint("api", __name__)


@api_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/login
    - Logs in a student using student_id and password.
    - Sets JWT as an HTTP-only cookie on success.
    - Request: {"student_id": "...", "password": "..."}
    - Example:
        curl -X POST http://localhost:8000/api/login -H "Content-Type: application/json" -d '{"student_id": "123", "password": "mypassword"}'
    """
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        raw_password = data.get("password")
        try:
            Student.query.filter_by(student_id=student_id).first()
        except Exception as e:
            current_app.logger.error(f"Database error: {e}")
            return internal_server_error()
        return login_controller(student_id, raw_password)
    except Exception as e:
        current_app.logger.error(f"{e}")
        return internal_server_error()


@api_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    """
    GET /api/logout
    - Logs out the current student (invalidates JWT).
    - JWT is read from cookie.
    - Example:
        curl -X GET http://localhost:8000/api/logout
    """
    try:
        jti = get_jwt()["jti"]
        return logout_controller(jti, jwt_blacklist)
    except:
        return internal_server_error()


@api_bp.route("/activate", methods=["POST"])
def activate():
    """
    POST /api/activate
    - Activates a student account using student_id, password, and OTP.
    - Request: {"student_id": "...", "password": "...", "otp": "..."}
    - Example:
        curl -X POST http://localhost:8000/api/activate -H "Content-Type: application/json" -d '{"student_id": "123", "password": "newpass", "otp": "123456"}'
    """
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
    """
    POST /api/forgot-password
    - Resets password using student_id, new password, and OTP.
    - Request: {"student_id": "...", "password": "...", "otp": "..."}
    - Example:
        curl -X POST http://localhost:8000/api/forgot-password -H "Content-Type: application/json" -d '{"student_id": "123", "password": "newpass", "otp": "123456"}'
    """
    try:
        data = request.get_json()
        student_id = data.get("student_id")
        raw_otp = data.get("otp")
        raw_password = data.get("password")
        return forget_password_controller(student_id, raw_otp, raw_password)
    except:
        return internal_server_error()


@api_bp.route("/send-otp", methods=["PATCH"])
def send_otp():
    """
    PATCH /api/send-otp?reason_id=1|2
    - Sends an OTP to the student's email for password change (1) or account activation (2).
    - Query Parameter: reason_id
    - Request: {"student_id": "..."}
    - Example:
        curl -X PATCH "http://localhost:8000/api/send-otp?reason_id=2" -H "Content-Type: application/json" -d '{"student_id": "123"}'
    """
    try:
        reason_id = request.args.get("reason_id")
        data = request.get_json()
        student_id = data.get("student_id")
        return send_otp_controller(student_id, reason_id)
    except:
        return internal_server_error()


@api_bp.route("/welcome", methods=["GET"])
@jwt_required()
def welcome():
    """
    GET /api/welcome
    - Returns the profile of the logged-in student (requires JWT in cookie).
    - Example:
        curl -X GET http://localhost:8000/api/welcome
    """
    try:
        student_id = get_jwt_identity()
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return welcome_controller(student)
    except:
        return internal_server_error()


@api_bp.route("/change-password", methods=["PATCH"])
@jwt_required()
def change_password():
    """
    PATCH /api/change-password
    - Changes the password for the logged-in student.
    - Requires JWT in cookie.
    - Request: {"old_password": "...", "new_password": "..."}
    - Example:
        curl -X PATCH http://localhost:8000/api/change-password -H "Content-Type: application/json" -d '{"old_password": "oldpass", "new_password": "newpass123"}'
    """
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return change_password_controller(student, old_password, new_password)
    except:
        return internal_server_error()


@api_bp.route("/list-semesters", methods=["GET"])
def list_semesters():
    try:
        return list_semesters_controller()
    except:
        return internal_server_error()


@api_bp.route("/university-info", methods=["GET"])
def university_info():
    try:
        return university_info_controller()
    except:
        return internal_server_error()


@api_bp.route("/class-schedule", methods=["GET"])
def class_schedule():
    try:
        student_id = request.args.get("student_id")
        season_id = request.args.get("season_id")
        year = request.args.get("year")

        return class_schedule_controller(student_id, season_id, year)
    except Exception as e:
        print(f"Error in /class-schedule: {e}")
        return internal_server_error()

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
    list_courses_controller,
    list_chosen_courses_controller,
    list_semesters_controller,
    select_course_controler,
    university_info_controller,
    class_schedule_controller,
    deselect_course_controler,
)
from app.models import Student


api_bp = Blueprint("api", __name__)


@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    student_id = data.get("student_id")
    raw_password = data.get("password")
    try:
        return login_controller(student_id, raw_password)
    except Exception as e:
        current_app.logger.error(f"{e}")
        return internal_server_error()


@api_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    try:
        return logout_controller(jti, jwt_blacklist)
    except:
        return internal_server_error()


@api_bp.route("/activate", methods=["POST"])
def activate():
    data = request.get_json()
    student_id = data.get("student_id")
    raw_otp = data.get("otp")
    raw_password = data.get("password")
    try:
        return activate_controller(student_id, raw_otp, raw_password)
    except:
        return internal_server_error()


@api_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    student_id = data.get("student_id")
    raw_otp = data.get("otp")
    raw_password = data.get("password")
    try:
        return forget_password_controller(student_id, raw_otp, raw_password)
    except:
        return internal_server_error()


@api_bp.route("/send-otp", methods=["PATCH"])
def send_otp():
    reason_id = request.args.get("reason_id")
    data = request.get_json()
    student_id = data.get("student_id")
    try:
        return send_otp_controller(student_id, reason_id)
    except:
        return internal_server_error()


@api_bp.route("/welcome", methods=["GET"])
@jwt_required()
def welcome():
    student_id = get_jwt_identity()
    try:
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
    student_id = get_jwt_identity()
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    try:
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
    student_id = request.args.get("student_id")
    season_id = request.args.get("season_id")
    year = request.args.get("year")
    try:
        is_able, res, student = relog_controller(student_id)  # type: ignore
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return class_schedule_controller(student, season_id, year)
    except Exception as e:
        print(f"Error in /class-schedule: {e}")
        return internal_server_error()


@api_bp.route("/list-courses", methods=["GET"])
@jwt_required()
def list_courses():
    student_id = get_jwt_identity()
    try:
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return list_courses_controller(student)
    except:
        return internal_server_error()


@api_bp.route("/list-chosen-courses", methods=["GET"])
@jwt_required()
def list_chosen_courses():
    student_id = get_jwt_identity()
    season_id = request.args.get("season_id")
    year = request.args.get("year")
    try:
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return list_chosen_courses_controller(student, season_id, year)
    except:
        return internal_server_error()


@api_bp.route("/select-course", methods=["PATCH"])
@jwt_required()
def select_course():
    student_id = get_jwt_identity()
    course_id = request.args.get("course_id")
    try:
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return select_course_controler(student, course_id)
    except:
        return internal_server_error()


@api_bp.route("/deselect-course", methods=["PATCH"])
@jwt_required()
def deselect_course():
    student_id = get_jwt_identity()
    course_id = request.args.get("course_id")
    try:
        is_able, res, student = relog_controller(student_id)
        if is_able is False or student is None:
            jti = get_jwt()["jti"]
            return logout_controller(jti, jwt_blacklist, res)
        return deselect_course_controler(student, course_id)
    except:
        return internal_server_error()

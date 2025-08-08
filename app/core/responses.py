from datetime import datetime, timezone
from typing import Literal
from flask import jsonify, Response, make_response


# General error responses
def missing_fields(fields) -> tuple[Response, Literal[400]]:
    return jsonify({"message": f"{', '.join(fields)} are required."}), 400


def invalid_value(field) -> tuple[Response, Literal[400]]:
    return jsonify({"message": f"Invalid value for {field}."}), 400


def student_not_exist() -> tuple[Response, Literal[404]]:
    return jsonify({"message": "Student does not exist."}), 404


def not_eligible(message) -> tuple[Response, Literal[401]]:
    return jsonify(message), 401


def account_not_activated() -> tuple[Response, Literal[401]]:
    return jsonify({"message": "Account is not activated."}), 401


def account_already_activated() -> tuple[Response, Literal[401]]:
    return jsonify({"message": "Account is already activated."}), 401


def invalid_password() -> tuple[Response, Literal[401]]:
    return jsonify({"message": "Invalid student_id or password."}), 401


def same_password() -> tuple[Response, Literal[401]]:
    return jsonify({"message": "choose a different password."}), 401


def password_too_short() -> tuple[Response, Literal[401]]:
    return (
        jsonify({"message": "Password must be greater than or equal to 8 characters."}),
        401,
    )


def invalid_otp() -> tuple[Response, Literal[401]]:
    return jsonify({"message": "Invalid OTP."}), 401


def error_creating_account(student_id) -> tuple[Response, Literal[500]]:
    return jsonify({"message": f"Error creating account: {student_id}"}), 500


def error_updating_password(student_id) -> tuple[Response, Literal[500]]:
    return jsonify({"message": f"Error updating password: {student_id}"}), 500


def error_generating_otp(student_id) -> tuple[Response, Literal[500]]:
    return jsonify({"message": f"Error generating OTP: {student_id}"}), 500


def error_sending_otp(student_id) -> tuple[Response, Literal[500]]:
    return jsonify({"message": f"Error sending OTP: {student_id}"}), 500


# Success responses
def login_success(access_token) -> Response:
    response = make_response(jsonify({"message": "Login successful", "access_token":access_token}), 200)
    return response


def logout_success(res) -> Response:
    response = make_response(res)
    response.delete_cookie("access_token_cookie")
    return response


def account_activated() -> tuple[Response, Literal[200]]:
    return jsonify({"message": "Account activated successfully."}), 200


def password_updated_successfully() -> tuple[Response, Literal[200]]:
    return jsonify({"message": "Password updated successfully."}), 200


def otp_sent() -> tuple[Response, Literal[200]]:
    return jsonify({"message": "OTP sent successfully."}), 200


def authentication_failed() -> tuple[Response, Literal[401]]:
    return (
        jsonify(
            {"message": "Authentication credentials were not provided or are invalid."}
        ),
        401,
    )


def internal_server_error() -> tuple[Response, Literal[500]]:
    return jsonify({"message": "Internal Server Error"}), 500


def account_locked(lockout_until) -> tuple[Response, Literal[403]]:
    return (
        jsonify({"message": f"Account is locked. Try again after {lockout_until}."}),
        403,
    )

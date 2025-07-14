from flask_jwt_extended import create_access_token

from app.core.responses import (
    invalid_otp,
    student_not_exist,
    not_eligible,
    account_not_activated,
    invalid_password,
    login_success,
    missing_fields,
    logout_success,
    password_too_short,
    account_already_activated,
)
from app.core.passwords import compare_password
from app.core.utils import (
    check_student_account,
    valid_str_req_value,
    check_student_login_ability,
)
from app.models.students import StudentOTP


def login_controller(student_id, raw_password):
    if valid_str_req_value([student_id, raw_password]) is False:
        return missing_fields(student_id, raw_password)

    student, student_login = check_student_account(student_id)
    if student is None:
        return student_not_exist()

    is_able, message = check_student_login_ability(student)
    if not is_able:
        return not_eligible(message)

    if student_login is None:
        return account_not_activated()

    if compare_password(raw_password, student_login.password) is False:
        return invalid_password()

    access_token = create_access_token(identity=student_id)
    return login_success(access_token)


def logout_controller(jti, jwt_blacklist):
    jwt_blacklist.add(jti)
    return logout_success()


def activate_controller(student_id, raw_otp, raw_password):
    if valid_str_req_value([student_id, raw_otp, raw_password]) is False:
        return missing_fields(student_id, raw_otp, raw_password)

    if len(raw_password) < 8:
        return password_too_short()

    student, student_login = check_student_account(student_id)
    if student is None:
        return student_not_exist()

    is_able, message = check_student_login_ability(student)
    if not is_able:
        return not_eligible(message)

    if student_login is not None:
        return account_already_activated()

    student_otp = StudentOTP.query.filter_by().first()
    if student_otp is None:
        return invalid_otp()

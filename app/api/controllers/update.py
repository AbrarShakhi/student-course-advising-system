from flask import current_app, request

from app.core.responses import (
    authentication_failed,
    error_updating_password,
    invalid_otp,
    password_updated_successfully,
    student_not_exist,
    not_eligible,
    account_not_activated,
    missing_fields,
    password_too_short,
    same_password,
)
from app.core.keys.passwords import hash_password, compare_password
from app.core.utils.std_manager import (
    check_student_account,
    valid_str_req_value,
    check_student_login_ability,
)
from app.core.keys.otp_manager import verify_otp
from app.core.db import save_db


def forget_password_controller(student_id, raw_otp, raw_password):
    if valid_str_req_value([student_id, raw_otp, raw_password]) is False:
        return missing_fields([student_id, raw_otp, raw_password])

    if len(raw_password) < 8:
        return password_too_short()

    student, student_login = check_student_account(student_id)
    if student is None:
        return student_not_exist()

    is_able, message = check_student_login_ability(student)
    if not is_able:
        return not_eligible(message)

    if student_login is None:
        return account_not_activated()

    if verify_otp(student_id, raw_otp) is False:
        return invalid_otp()

    student_login.password = hash_password(raw_password)
    if save_db(student_login) is False:
        return error_updating_password(student_id)

    current_app.logger.info(
        f"[AUDIT] Password reset for student_id={student_id} from {request.remote_addr}"
    )
    return password_updated_successfully()


def change_password_controller(student_id, old_password, new_password):
    if valid_str_req_value([student_id]) is False:
        return authentication_failed()

    if valid_str_req_value([new_password, old_password]) is False:
        return missing_fields([new_password, old_password])

    if len(new_password) < 8:
        return password_too_short()

    student, student_login = check_student_account(student_id)
    if student is None:
        return student_not_exist()

    is_able, message = check_student_login_ability(student)
    if not is_able:
        return not_eligible(message)

    if student_login is None:
        return account_not_activated()

    # Check that the old password matches before allowing change
    if not compare_password(old_password, student_login.password):
        return same_password()

    student_login.password = hash_password(new_password)
    if save_db(student_login) is False:
        return error_updating_password(student_id)

    current_app.logger.info(
        f"[AUDIT] Password changed for student_id={student_id} from {request.remote_addr}"
    )
    return password_updated_successfully()

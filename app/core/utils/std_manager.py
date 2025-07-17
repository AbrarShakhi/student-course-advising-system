from datetime import datetime, timedelta, timezone

from flask import current_app

from app.core.serializers.base import serialize_credit_partition
from app.models.base import University
from app.models.students import Student, StudentLogin
from app.core.db import save_db
from app.core.utils.helpers import get_uni_info


def check_student_login_ability(student: Student) -> tuple[bool, dict]:
    if student.is_dismissed:
        return False, {"message": "You are dismissed from the university."}
    if student.is_graduated:
        return False, {"message": "You have graduated from the university."}
    uni_info = get_uni_info()

    if uni_info.is_advising is True:
        if uni_info.min_cred is None or uni_info.max_cred is None:
            current_app.logger.error(f"[AUDIT] In database table:'university' error.")
            raise Exception
        if not (uni_info.min_cred <= student.credit_completed <= uni_info.max_cred):
            return False, {"message": "It is not your advising time"}
    return True, {}


def check_student_account(
    student_id: str,
) -> tuple[Student | None, StudentLogin | None]:
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return None, None
    student_login = StudentLogin.query.filter_by(student_id=student_id).first()
    return student, student_login


def valid_str_req_value(values=None):
    if type(values) != list:
        raise TypeError

    for value in values:
        if value is None:
            return False
        if len(value) == 0:
            return False
        if type(value) != str:
            return False

    return True


def check_std_lockout(student_login):
    if student_login.lockout_until:
        now = datetime.now(timezone.utc)
        lockout_until = student_login.lockout_until
        if lockout_until.tzinfo is None:
            lockout_until = lockout_until.replace(tzinfo=timezone.utc)
        if lockout_until > now:
            return False
    return True


def increment_std_false_attempts(student_login, look_after=5, look_duration=15):
    student_login.failed_attempts = (student_login.failed_attempts or 0) + 1
    if student_login.failed_attempts >= look_after:
        student_login.lockout_until = datetime.now(timezone.utc) + timedelta(
            minutes=look_duration
        )
        student_login.failed_attempts = 0
    save_db(student_login)

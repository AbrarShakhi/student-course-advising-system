from datetime import datetime, timedelta, timezone

from app.models.students import Student, StudentLogin
from app.core.db import save_db


def check_student_login_ability(student: Student) -> tuple[bool, dict]:
    if student.is_dismissed:
        return False, {"message": "You are dismissed from the university."}
    if student.is_graduated:
        return False, {"message": "You have graduated from the university."}
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
        if student_login.lockout_until > now:
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

from common.try_catch import try_catch

from .models import Student, StudentLogin


def check_student_login_ability(student: Student) -> tuple[bool, dict]:
    if student.is_dismissed:
        return False, {"message": "You are dismissed from the university."}
    if student.is_graduated:
        return False, {"message": "You have graduated from the university."}
    return True, {}


def check_student_account(
    student_id: str,
) -> tuple[Student | None, StudentLogin | None]:
    student, err = try_catch(Student.objects.get, student_id=student_id)
    if err.not_ok() and err.is_type(Student.DoesNotExist):
        return None, None

    student_login, err = try_catch(StudentLogin.objects.get, student=student)
    if err.not_ok() and err.is_type(StudentLogin.DoesNotExist):
        return student, None

    return student, student_login

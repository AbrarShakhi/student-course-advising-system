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
    student, student_login = None, None
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        return None, None

    try:
        student_login = StudentLogin.objects.get(student=student)
    except StudentLogin.DoesNotExist:
        return student, None

    return student, student_login

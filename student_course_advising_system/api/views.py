from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.emailer import Emailer
from common.hashing import hash_password
from common import responses

from .utils import check_student_account, check_student_login_ability
from .models import StudentLogin, StudentOtp
from .serializers import StudentSerializer


class LoginStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        raw_password = request.data.get("password")
        if not student_id or not raw_password:
            return responses.missing_fields(["student_id", "password"])

        student, student_login = check_student_account(student_id)
        if student is None:
            return responses.student_not_exist()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        if student_login is None:
            return responses.account_not_activated()

        if not student_login.check_password(raw_password):
            return responses.invalid_password()

        response = responses.login_success()
        response.set_cookie("student_id", student_id, httponly=True)
        return response


class LogoutStudent(APIView):
    def get(self, format=None):
        response = responses.logout_success()
        response.delete_cookie("student_id")
        return response


class ActivateStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        raw_otp = request.data.get("otp")
        raw_password = request.data.get("password")
        if not student_id or not raw_password or not raw_otp:
            return responses.missing_fields(["student_id", "password", "otp"])

        if len(raw_password) < 8:
            return responses.password_too_short()

        student, student_login = check_student_account(student_id)
        if student is None:
            return responses.student_not_exist()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        if student_login is not None:
            return responses.account_already_activated()

        try:
            student_otp = StudentOtp.objects.get(student=student)
        except StudentOtp.DoesNotExist:
            return responses.invalid_otp()
        if student_otp.compare_otp(raw_otp) is False:
            return responses.invalid_otp()

        try:
            StudentLogin.objects.update_or_create(
                student=student, defaults={"password": hash_password(raw_password)}
            )
        except Exception as e:
            return responses.error_creating_account(student_id)

        return responses.account_activated()


class ForgotPassword(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        raw_otp = request.data.get("otp")
        raw_password = request.data.get("password")

        if not student_id or not raw_otp or not raw_password:
            return responses.missing_fields(["student_id", "otp", "password"])

        if len(raw_password) < 8:
            return responses.password_too_short()

        student, student_login = check_student_account(student_id)
        if student is None:
            return responses.student_not_exist()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        if student_login is None:
            return responses.account_not_activated()

        try:
            student_otp = StudentOtp.objects.get(student=student)
        except StudentOtp.DoesNotExist:
            return responses.invalid_otp()
        if student_otp.compare_otp(raw_otp) is False:
            return responses.invalid_otp()

        try:
            student_login.password = hash_password(raw_password)
            student_login.save()
        except Exception as e:
            return responses.error_updating_password(student_id)

        return responses.password_updated_successfully()


class SendOTP(APIView):
    reason_ids = {1: "change_password", 2: "activate_account"}

    def patch(self, request, format=None):
        student_id = request.data.get("student_id")
        reason_id = request.GET.get("reason_id")
        if not student_id or not reason_id:
            return responses.missing_fields(["student_id", "reason_id"])

        try:
            reason_id = int(reason_id)
        except ValueError:
            return responses.invalid_value("reason_id")

        if reason_id not in self.reason_ids.keys():
            return responses.invalid_value("reason_id")

        student, student_login = check_student_account(student_id)
        if student is None:
            return responses.student_not_exist()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        if reason_id == 2:
            if student_login is not None:
                return responses.account_already_activated()
        elif reason_id == 1:
            if student_login is None:
                return responses.account_not_activated()

        try:
            try:
                student_otp = StudentOtp.objects.get(student=student)
            except StudentOtp.DoesNotExist:
                try:
                    student_otp = StudentOtp.objects.create(student=student)
                except Exception:
                    return responses.error_generating_otp(student_id)

            if student_otp is None:
                return responses.error_generating_otp(student_id)

            db_otp = student_otp.get_otp()
            if db_otp is None:
                return responses.error_generating_otp(student_id)
        except Exception:
            return responses.error_generating_otp(student_id)

        emailer = Emailer(student.email, self.reason_ids[reason_id])

        # FIX: FIX THE EMAIl 
        print(db_otp)
        # try:
        #     emailer.send(db_otp)
        # except Exception as e:
        #     return responses.error_sending_otp(student_id)

        return responses.otp_sent()


class ChangePassword(APIView):
    def patch(self, request, format=None):
        student_id = request.COOKIES.get("student_id")
        old_raw_password = request.data.get("old_password")
        new_raw_password = request.data.get("new_password")
        if not old_raw_password or not new_raw_password:
            return responses.missing_fields(["old_password", "new_password"])

        if not student_id:
            return responses.authentication_failed()

        student, student_login = check_student_account(student_id)
        if student is None or student_login is None:
            return responses.authentication_failed()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        if len(new_raw_password) < 8:
            return responses.password_too_short()

        if student_login.check_password(old_raw_password) is False:
            return responses.invalid_password()

        try:
            student_login.password = hash_password(new_raw_password)
            student_login.save()
        except Exception as e:
            return responses.error_updating_password(student_id)

        return responses.password_updated_successfully()


class Home(APIView):
    def get(self, request, format=None):
        student_id = request.COOKIES.get("student_id")
        if not student_id:
            return responses.authentication_failed()

        student, student_login = check_student_account(student_id)
        if student is None or student_login is None:
            return responses.authentication_failed()

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return responses.not_eligible(message)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

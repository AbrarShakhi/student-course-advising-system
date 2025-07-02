from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from django.conf import settings

from common.try_catch import try_catch
from common.emailer import Emailer

from .utils import check_student_login_ability, check_student_account
from .models import StudentLogin, StudentOtp


class LoginStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        raw_password = request.data.get("password")
        if not student_id or not raw_password:
            return Response(
                {"message": "student_id and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student, student_login = check_student_account(student_id)
        if student is None:
            return Response(
                {"message": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        if student_login is None:
            return Response(
                {"message": "Account is not activated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not student_login.check_password(raw_password):
            return Response(
                {"message": "Invalid student_id or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        response.set_cookie("student_id", student_id, httponly=True)
        return response


class LogoutStudent(APIView):
    def get(self, format=None):
        response = Response(
            {"message": "Logout successful."}, status=status.HTTP_200_OK
        )
        response.delete_cookie("student_id")
        return response


class ActivateStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        raw_otp = request.data.get("otp")
        raw_password = request.data.get("password")
        if not student_id or not raw_password or not raw_otp:
            return Response(
                {"message": "student_id and password and otp are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(raw_password) <= 8:
            return Response(
                {"message": "Password must be greater than 8 characters."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        student, student_login = check_student_account(student_id)
        if student is None:
            return Response(
                {"message": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        if student_login is not None:
            return Response(
                {"message": "Account is already activated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        student_otp, err = try_catch(StudentOtp.objects.get, student=student)
        if err.not_ok() or not student_otp.compare_otp(raw_otp):
            return Response(
                {"message": "Invalid OTP."}, status=status.HTTP_401_UNAUTHORIZED
            )

        _, err = try_catch(
            StudentLogin.objects.update_or_create,
            student=student,
            defaults={"password": make_password(raw_password)},
        )
        if err.not_ok():
            return Response(
                {"message": f"Error creating account: {student_id}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Account activated successfully."}, status=status.HTTP_200_OK
        )


class SendOTP(APIView):
    reason_ids = {1: "change_password", 2: "activate_account"}

    def patch(self, request, format=None):
        student_id = request.data.get("student_id")
        reason_id = request.GET.get("reason_id")
        if not student_id or not reason_id:
            return Response(
                {"message": "student_id and reason_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason_id, err = try_catch(int, reason_id)
        if err.not_ok() or reason_id not in self.reason_ids.keys():
            return Response(
                {"message": "Invalid reason_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student, student_login = check_student_account(student_id)
        if student is None:
            return Response(
                {"message": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        is_able, message = check_student_login_ability(student)
        if not is_able:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        student_otp, err = try_catch(StudentOtp.objects.get, student=student)
        if err.not_ok() and err.is_type(StudentOtp.DoesNotExist):
            student_otp, err = try_catch(StudentOtp.objects.create, student=student)
            if err.not_ok():
                return Response(
                    {"message": f"Error creating OTP: {student_id}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        student_otp.refresh_otp()
        db_otp = student_otp.get_otp()

        emailer, err = try_catch(Emailer, student.email, self.reason_ids[reason_id])
        if err.not_ok():
            return Response(
                {"message": f"Error sending OTP: {student_id}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        _, err = try_catch(emailer.send, db_otp)
        if err.not_ok():
            print(f"Error sending OTP: {err}")
            return Response(
                {"message": f"Error sending OTP: {student_id}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"message": "OTP sent successfully."}, status=status.HTTP_200_OK
        )

from rest_framework.response import Response
from rest_framework import status


# General error responses
def missing_fields(fields):
    return Response(
        {"message": f"{', '.join(fields)} are required."},
        status=status.HTTP_400_BAD_REQUEST,
    )


def invalid_value(field):
    return Response(
        {"message": f"Invalid value for {field}."}, status=status.HTTP_400_BAD_REQUEST
    )


def student_not_exist():
    return Response(
        {"message": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
    )


def not_eligible(message):
    return Response(message, status=status.HTTP_401_UNAUTHORIZED)


def account_not_activated():
    return Response(
        {"message": "Account is not activated."}, status=status.HTTP_401_UNAUTHORIZED
    )


def account_already_activated():
    return Response(
        {"message": "Account is already activated."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


def invalid_password():
    return Response(
        {"message": "Invalid student_id or password."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


def password_too_short():
    return Response(
        {"message": "Password must be greater than or equal to 8 characters."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


def invalid_otp():
    return Response({"message": "Invalid OTP."}, status=status.HTTP_401_UNAUTHORIZED)


def error_creating_account(student_id):
    return Response(
        {"message": f"Error creating account: {student_id}"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def error_generating_otp(student_id):
    return Response(
        {"message": f"Error generating OTP: {student_id}"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def error_sending_otp(student_id):
    return Response(
        {"message": f"Error sending OTP: {student_id}"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# Success responses
def login_success():
    return Response({"message": "Login successful."}, status=status.HTTP_200_OK)


def logout_success():
    return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


def account_activated():
    return Response(
        {"message": "Account activated successfully."}, status=status.HTTP_200_OK
    )


def otp_sent(db_otp):
    return Response(
        {"message": "OTP sent successfully.", "opt": db_otp}, status=status.HTTP_200_OK
    )

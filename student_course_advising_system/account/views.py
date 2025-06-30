from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudentLogin
from .serializers import StudentLoginSerializer
from django.contrib.auth.hashers import check_password, make_password
from .models import Student


class LoginStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        password = request.data.get("password")
        if not student_id or not password:
            return Response(
                {"detail": "student_id and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            student_login = StudentLogin.objects.get(student=student)
        except StudentLogin.DoesNotExist:
            return Response(
                {"detail": "Account does not exist."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, student_login.password):
            return Response(
                {"detail": "Invalid student_id or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
        response.set_cookie("student_id", student_id, httponly=True)
        return response


class LogoutStudent(APIView):
    def get(self, format=None):
        response = Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        response.delete_cookie("student_id")
        return response


class ActivateStudent(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("student_id")
        password = request.data.get("password")

        if not student_id or not password:
            return Response(
                {"detail": "student_id and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) <= 8:
            return Response(
                {"detail": "Password must be greater than 8 characters."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        if student.is_dismissed:
            return Response(
                {"detail": "Student is dismissed."}, status=status.HTTP_401_UNAUTHORIZED
            )
        if student.is_graduated:
            return Response(
                {"detail": "Student is graduated."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if StudentLogin.objects.filter(student=student).exists():
            return Response(
                {"detail": "Account is already activated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        hashed_password = make_password(password)

        try:
            StudentLogin.objects.update_or_create(
                student=student,
                defaults={"password": hashed_password},
            )
        except StudentLogin.errors as e:
            return Response(
                print(e),
                {"detail": f"Error creating account: {student_id}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": "Account activated successfully."}, status=status.HTTP_200_OK
        )

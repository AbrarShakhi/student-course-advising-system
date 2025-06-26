from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudentLogin
from .serializers import StudentLoginSerializer
from django.contrib.auth.hashers import check_password


class TestView(APIView):
    def get(self, request, format=None):
        return Response({"name": "abrar"})


class LoginView(APIView):
    def post(self, request):
        studentId = request.data.get("studentId")
        password = request.data.get("password")
        try:
            student = StudentLogin.objects.get(studentId=studentId)
            if student.password != password:  # For real apps, use hashed passwords!
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer = StudentLoginSerializer(student)
            return Response(
                {"message": "Login successful", "student": serializer.data},
                status=status.HTTP_200_OK,
            )
        except StudentLogin.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

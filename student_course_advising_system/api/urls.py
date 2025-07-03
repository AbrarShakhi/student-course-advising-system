from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# Authentication Endpoints
# ------------------------
authentication_patterns = [
    # =============================
    # POST /api/login
    # - Logs in a student using student_id and password.
    # - Request: {"student_id": "...", "password": "..."}
    # - Example:
    #     curl -X POST http://localhost:8000/api/login -H "Content-Type: application/json" -d '{"student_id": "123", "password": "mypassword"}'
    # =============================
    path("login", views.LoginStudent.as_view(), name="LoginStudent"),

    # =============================
    # GET /api/logout
    # - Logs out the current student (removes student_id cookie).
    # - Example:
    #     curl -X GET http://localhost:8000/api/logout --cookie "student_id=123"
    # =============================
    path("logout", views.LogoutStudent.as_view(), name="LogoutStudent"),

    # =============================
    # POST /api/activate
    # - Activates a student account using student_id, password, and OTP.
    # - Request: {"student_id": "...", "password": "...", "otp": "..."}
    # - Example:
    #     curl -X POST http://localhost:8000/api/activate -H "Content-Type: application/json" -d '{"student_id": "123", "password": "newpass", "otp": "123456"}'
    # =============================
    path("activate", views.ActivateStudent.as_view(), name="ActivateStudent"),

    # =============================
    # POST /api/forgot-password
    # - Resets password using student_id, new password, and OTP.
    # - Request: {"student_id": "...", "password": "...", "otp": "..."}
    # - Example:
    #     curl -X POST http://localhost:8000/api/forgot-password -H "Content-Type: application/json" -d '{"student_id": "123", "password": "newpass", "otp": "123456"}'
    # =============================
    path("forgot-password", views.ForgotPassword.as_view(), name="ForgotPassword"),

    # =============================
    # PATCH /api/send-otp?reason_id=1|2
    # - Sends an OTP to the student's email for password change (1) or account activation (2).
    # - Request: {"student_id": "..."}
    # - Example:
    #     curl -X PATCH "http://localhost:8000/api/send-otp?reason_id=2" -H "Content-Type: application/json" -d '{"student_id": "123"}'
    # =============================
    path("send-otp", views.SendOTP.as_view(), name="SendOTP"),
]

# Home/Profile & Password Management Endpoints
# --------------------------------------------
home_patterns = [
    # =============================
    # PATCH /api/change-password
    # - Changes the password for the logged-in student.
    # - Requires student_id cookie.
    # - Request: {"old_password": "...", "new_password": "..."}
    # - Example:
    #     curl -X PATCH http://localhost:8000/api/change-password -H "Content-Type: application/json" --cookie "student_id=123" -d '{"old_password": "oldpass", "new_password": "newpass123"}'
    # =============================
    path("change-password", views.ChangePassword.as_view(), name="ChangePassword"),

    # =============================
    # GET /api/home
    # - Returns the profile of the logged-in student (requires student_id cookie).
    # - Example:
    #     curl -X GET http://localhost:8000/api/home --cookie "student_id=123"
    # =============================
    path("home", views.Home.as_view(), name="Home"),
]

urlpatterns = authentication_patterns + home_patterns
urlpatterns = format_suffix_patterns(urlpatterns)

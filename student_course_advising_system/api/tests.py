from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Student, StudentLogin, StudentOtp
from common.hashing import hash_password

class StudentAPITestCase(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id="S12345678901",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_no="1234567890",
            guardian_name="Jane Doe",
            guardian_phone="0987654321",
            is_dismissed=False,
            is_graduated=False,
        )
        self.password = "testpassword"
        self.login = StudentLogin.objects.create(
            student=self.student, password=hash_password(self.password)
        )
        self.otp = StudentOtp.objects.create(student=self.student)
        self.otp.reset_otp()
        self.otp_value = self.otp.otp

    def test_login_success(self):
        url = reverse("LoginStudent")
        data = {"student_id": self.student.student_id, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("student_id", response.cookies)
        self.assertEqual(response.data["message"], "Login successful.")

    def test_login_missing_fields(self):
        url = reverse("LoginStudent")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("are required.", response.data["message"])

    def test_login_wrong_password(self):
        url = reverse("LoginStudent")
        data = {"student_id": self.student.student_id, "password": "wrongpass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Invalid student_id or password.")

    def test_login_not_activated(self):
        self.login.delete()
        url = reverse("LoginStudent")
        data = {"student_id": self.student.student_id, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Account is not activated.")

    def test_login_student_not_exist(self):
        url = reverse("LoginStudent")
        data = {"student_id": "NOPE", "password": "whatever"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Student does not exist.")

    def test_login_not_eligible(self):
        self.student.is_dismissed = True
        self.student.save()
        url = reverse("LoginStudent")
        data = {"student_id": self.student.student_id, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("dismissed", response.data["message"])

    def test_logout_success(self):
        url = reverse("LogoutStudent")
        self.client.cookies["student_id"] = self.student.student_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful.")
        self.assertEqual(response.cookies["student_id"].value, "")

    def test_activate_success(self):
        self.login.delete()  # must not be activated
        url = reverse("ActivateStudent")
        data = {
            "student_id": self.student.student_id,
            "password": "newpassword123",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Account activated successfully.")
        self.assertTrue(StudentLogin.objects.filter(student=self.student).exists())

    def test_activate_missing_fields(self):
        url = reverse("ActivateStudent")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_password_too_short(self):
        self.login.delete()
        url = reverse("ActivateStudent")
        data = {
            "student_id": self.student.student_id,
            "password": "short",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Password must be greater", response.data["message"])

    def test_activate_already_activated(self):
        url = reverse("ActivateStudent")
        data = {
            "student_id": self.student.student_id,
            "password": "newpassword123",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("already activated", response.data["message"])

    def test_activate_invalid_otp(self):
        self.login.delete()
        url = reverse("ActivateStudent")
        data = {
            "student_id": self.student.student_id,
            "password": "newpassword123",
            "otp": "000000",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid OTP", response.data["message"])

    def test_activate_student_not_exist(self):
        self.login.delete()
        url = reverse("ActivateStudent")
        data = {
            "student_id": "NOPE",
            "password": "newpassword123",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activate_not_eligible(self):
        self.login.delete()
        self.student.is_graduated = True
        self.student.save()
        url = reverse("ActivateStudent")
        data = {
            "student_id": self.student.student_id,
            "password": "newpassword123",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("graduated", response.data["message"])

    def test_forgot_password_success(self):
        url = reverse("ForgotPassword")
        data = {
            "student_id": self.student.student_id,
            "password": "resetpassword",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password updated successfully.")
        self.login.refresh_from_db()
        self.assertTrue(self.login.check_password("resetpassword"))

    def test_forgot_password_missing_fields(self):
        url = reverse("ForgotPassword")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_password_too_short(self):
        url = reverse("ForgotPassword")
        data = {
            "student_id": self.student.student_id,
            "password": "short",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Password must be greater", response.data["message"])

    def test_forgot_password_account_not_activated(self):
        self.login.delete()
        url = reverse("ForgotPassword")
        data = {
            "student_id": self.student.student_id,
            "password": "resetpassword",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("not activated", response.data["message"])

    def test_forgot_password_invalid_otp(self):
        url = reverse("ForgotPassword")
        data = {
            "student_id": self.student.student_id,
            "password": "resetpassword",
            "otp": "000000",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid OTP", response.data["message"])

    def test_forgot_password_student_not_exist(self):
        url = reverse("ForgotPassword")
        data = {
            "student_id": "NOPE",
            "password": "resetpassword",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_forgot_password_not_eligible(self):
        self.student.is_dismissed = True
        self.student.save()
        url = reverse("ForgotPassword")
        data = {
            "student_id": self.student.student_id,
            "password": "resetpassword",
            "otp": self.otp_value,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("dismissed", response.data["message"])

    @patch("common.emailer.Emailer.send")
    def test_send_otp_success_activate(self, mock_send):
        self.login.delete()
        url = reverse("SendOTP") + "?reason_id=2"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent successfully.", response.data["message"])
        mock_send.assert_called()

    @patch("common.emailer.Emailer.send")
    def test_send_otp_success_change_password(self, mock_send):
        url = reverse("SendOTP") + "?reason_id=1"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP sent successfully.", response.data["message"])
        mock_send.assert_called()

    def test_send_otp_missing_fields(self):
        url = reverse("SendOTP") + "?reason_id=1"
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_otp_invalid_reason(self):
        url = reverse("SendOTP") + "?reason_id=99"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid value for reason_id", response.data["message"])

    def test_send_otp_account_already_activated(self):
        url = reverse("SendOTP") + "?reason_id=2"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("already activated", response.data["message"])

    def test_send_otp_account_not_activated(self):
        self.login.delete()
        url = reverse("SendOTP") + "?reason_id=1"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("not activated", response.data["message"])

    def test_send_otp_student_not_exist(self):
        url = reverse("SendOTP") + "?reason_id=1"
        data = {"student_id": "NOPE"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_otp_not_eligible(self):
        self.student.is_graduated = True
        self.student.save()
        url = reverse("SendOTP") + "?reason_id=1"
        data = {"student_id": self.student.student_id}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("graduated", response.data["message"])

    def test_change_password_success(self):
        url = reverse("ChangePassword")
        self.client.cookies["student_id"] = self.student.student_id
        data = {"old_password": self.password, "new_password": "newpass123"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password updated successfully.")
        self.login.refresh_from_db()
        self.assertTrue(self.login.check_password("newpass123"))

    def test_change_password_missing_fields(self):
        url = reverse("ChangePassword")
        self.client.cookies["student_id"] = self.student.student_id
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_short_password(self):
        url = reverse("ChangePassword")
        self.client.cookies["student_id"] = self.student.student_id
        data = {"old_password": self.password, "new_password": "short"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Password must be greater", response.data["message"])

    def test_change_password_wrong_old_password(self):
        url = reverse("ChangePassword")
        self.client.cookies["student_id"] = self.student.student_id
        data = {"old_password": "wrongpass", "new_password": "newpass123"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid student_id or password", response.data["message"])

    def test_change_password_not_authenticated(self):
        url = reverse("ChangePassword")
        data = {"old_password": self.password, "new_password": "newpass123"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Authentication credentials were not provided", response.data["message"])

    def test_change_password_not_eligible(self):
        self.student.is_dismissed = True
        self.student.save()
        url = reverse("ChangePassword")
        self.client.cookies["student_id"] = self.student.student_id
        data = {"old_password": self.password, "new_password": "newpass123"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("dismissed", response.data["message"])

    def test_home_success(self):
        url = reverse("Home")
        self.client.cookies["student_id"] = self.student.student_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["student_id"], self.student.student_id)
        self.assertEqual(response.data["first_name"], self.student.first_name)
        self.assertEqual(response.data["last_name"], self.student.last_name)

    def test_home_not_authenticated(self):
        url = reverse("Home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Authentication credentials were not provided", response.data["message"])

    def test_home_not_eligible(self):
        self.student.is_graduated = True
        self.student.save()
        url = reverse("Home")
        self.client.cookies["student_id"] = self.student.student_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("graduated", response.data["message"])


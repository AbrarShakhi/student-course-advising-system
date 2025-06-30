import random
import string
from datetime import timedelta

from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone


class Student(models.Model):
    student_id = models.CharField(max_length=13, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, unique=True)
    guardian_name = models.CharField(max_length=128)
    guardian_phone = models.CharField(max_length=20)
    is_dismissed = models.BooleanField(default=False)
    is_graduated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"


class StudentLogin(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, primary_key=True, related_name="id"
    )
    password = models.CharField(max_length=128)

    def change_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.student.student_id}"


class StudentOtp(models.Model):
    MAX_TRIES = 5

    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, primary_key=True, related_name="otp"
    )
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    try_count = models.PositiveIntegerField(default=0)

    def generate_otp(self):
        return "".join(random.choices(string.digits, k=6))

    def create_or_refresh_otp(self):
        now = timezone.now()

        if (
            not self.otp
            or not self.created_at
            or not self.expires_at
            or not self.try_count
        ):
            self.otp = self.generate_otp()
            self.created_at = now
            self.expires_at = now + timedelta(minutes=10)
            self.try_count = 0
            self.save()

    def increment_try_count(self):
        self.try_count += 1
        self.save()

    def is_expired(self):
        return (
            not self.expires_at
            or timezone.now() > self.expires_at
            or self.try_count >= self.MAX_TRIES
        )

    def __str__(self):
        status = "Expired" if self.is_expired() else "Active"
        return f"OTP for {self.student.student_id} - {status} (Tries: {self.try_count})"

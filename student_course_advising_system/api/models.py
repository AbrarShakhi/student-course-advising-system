import random
import string
from datetime import timedelta

from django.db import models
from django.utils import timezone

from common.hashing import hash_password, compare_password


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
        self.password = hash_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return compare_password(raw_password, self.password)

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

    def reset_otp(self):
        now = timezone.now()
        self.otp = self.generate_otp()
        self.created_at = now
        self.expires_at = now + timedelta(minutes=10)
        self.try_count = 0
        self.save()

    def refresh_otp(self):
        if (
            self.otp is None
            or self.created_at is None
            or self.expires_at is None
            or self.try_count is None
        ):
            self.reset_otp()

        if self.is_expired():
            self.reset_otp()

    def get_otp(self):
        self.refresh_otp()
        return self.otp

    def compare_otp(self, raw_otp):
        if self.otp is None or self.created_at is None or self.expires_at is None:
            return False

        if self.get_otp() == raw_otp:
            self.otp = None
            self.created_at = None
            self.expires_at = None
            self.try_count = 0
            self.save()
            return True
        else:
            self.increment_try_count()
            return False

    def increment_try_count(self):
        self.try_count = self.try_count + 1
        self.save()

    def is_expired(self):
        return (
            self.expires_at is None
            or timezone.now() > self.expires_at
            or self.try_count >= self.MAX_TRIES
        )

    def __str__(self):
        status = "Expired" if self.is_expired() else "Active"
        return f"OTP for {self.student.student_id} - {status} (Tries: {self.try_count})"

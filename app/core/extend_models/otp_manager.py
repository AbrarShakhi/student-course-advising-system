import random
import string
from datetime import timedelta

from app.models.students import StudentOTP


class OtpManager(StudentOTP):
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

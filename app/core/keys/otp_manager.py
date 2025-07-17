import random
import string
from datetime import datetime, timedelta

from app.models.students import StudentOTP
from app.core.db import save_db


def generate_otp(length: int = 6):
    """Generates a random numerical OTP."""
    return "".join(random.choices(string.digits, k=length))


def verify_otp(student_id: str, raw_otp: str):
    """Verifies a given OTP for a student."""
    student_otp = StudentOTP.query.filter_by(student_id=student_id).first()
    if student_otp is None:
        return False

    return OtpManager(student_otp).compare_otp(raw_otp)


class OtpManager:
    """Manages OTP generation, validation, and expiration logic."""
    MAX_TRIES = 5

    def __init__(self, std_otp: StudentOTP):
        self.__std_otp: StudentOTP = std_otp
        # The initial refresh is called to ensure the OTP state is valid.
        self.__refresh_otp()

    def __reset_otp(self):
        """Resets the OTP with a new value, creation time, and expiration time."""
        # Use datetime.utcnow() to get a naive datetime object in UTC.
        now = datetime.utcnow()
        self.__std_otp.otp = generate_otp()
        self.__std_otp.created_at = now
        self.__std_otp.expires_at = now + timedelta(minutes=10)
        self.__std_otp.try_count = 0
        save_db(self.__std_otp)

    def __refresh_otp(self):
        """Refreshes the OTP if it's missing or expired."""
        # Check if any of the core OTP fields are not set.
        if (
            self.__std_otp.otp is None
            or self.__std_otp.created_at is None
            or self.__std_otp.expires_at is None
            or self.__std_otp.try_count is None
        ):
            self.__reset_otp()
        # Also reset if the OTP is expired.
        if self.is_expired():
            self.__reset_otp()

    def get_otp(self):
        """Returns the current valid OTP."""
        self.__refresh_otp()
        return self.__std_otp.otp

    def compare_otp(self, raw_otp):
        """Compares the raw OTP with the stored OTP and handles success/failure."""
        if (
            self.__std_otp.otp is None
            or self.__std_otp.created_at is None
            or self.__std_otp.expires_at is None
        ):
            return False
            
        # Use get_otp() to ensure the OTP isn't expired before comparing.
        if self.get_otp() == raw_otp:
            # On successful verification, invalidate the OTP.
            self.__std_otp.otp = None
            self.__std_otp.created_at = None
            self.__std_otp.expires_at = None
            self.__std_otp.try_count = 0
            return save_db(self.__std_otp)
        else:
            # On failure, increment the try count.
            self.__increment_try_count()
            return False

    def __increment_try_count(self):
        """Increments the attempt counter."""
        self.__std_otp.try_count = (self.__std_otp.try_count or 0) + 1
        save_db(self.__std_otp)

    def is_expired(self):
        """Checks if the OTP has expired due to time or too many attempts."""
        return (
            self.__std_otp.expires_at is None
            # FIX: Compare naive datetime from DB with a naive UTC datetime.
            or datetime.utcnow() > self.__std_otp.expires_at
            or (self.__std_otp.try_count or 0) >= self.MAX_TRIES
        )

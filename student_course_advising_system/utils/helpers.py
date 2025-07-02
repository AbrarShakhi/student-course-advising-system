import yagmail


subject = f"Your OTP for {self.reason_ids[reason_id]}"
body = f"Dear {student.name},\n\nYour OTP for {self.reason_ids[reason_id]} is: {otp}\n\nRegards,\nYour Team"

try:
    # Initialize yagmail.SMTP client
    yag = yagmail.SMTP(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
    # Send email
    yag.send(to=student.email, subject=subject, contents=body)
except Exception as e:
    return Response(
        {"message": f"Failed to send email: {str(e)}"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

return Response(
    {"message": f"OTP sent successfully to {student.email}."},
    status=status.HTTP_200_OK,
)


class ErrorWrapper:
    def __init__(self, error):
        self.error = error

    def not_ok(self):
        return self.error is not None

    def ok(self):
        return self.error is None

    def is_type(self, exc_type):
        return isinstance(self.error, exc_type)

    def get_error(self):
        return self.error

    def __bool__(self):
        return self.error is None

    def __str__(self):
        return str(self.error)


def try_catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), ErrorWrapper(None)
    except Exception as err:
        return None, ErrorWrapper(err)

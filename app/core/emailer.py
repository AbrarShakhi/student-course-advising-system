import yagmail
from flask import current_app

REASON_SUBJECTS = {
    "change_password": "Password Reset Code",
    "activate_account": "Account Activation Code",
}


class Emailer:
    def __init__(self, sender: str, reason: str) -> None:
        self.sender = sender
        self.reason = reason
        self.subject = REASON_SUBJECTS.get(self.reason)
        self.yag = yagmail.SMTP(
            current_app.config["EMAIL_ADDRESS"], current_app.config["EMAIL_PASSWORD"]
        )

    def send(self, code: str) -> None:
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f9f9f9; padding: 30px; }}
                .container {{ background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; max-width: 400px; margin: auto; padding: 24px; }}
                .reason {{ color: #333; font-size: 18px; margin-bottom: 16px; }}
                .code {{ font-size: 32px; color: #1976d2; font-weight: bold; letter-spacing: 2px; background: #f0f4ff; padding: 12px 24px; border-radius: 6px; display: inline-block; margin-bottom: 16px; }}
                .footer {{ color: #888; font-size: 12px; margin-top: 24px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="reason">Your code for <b>{self.reason.replace('_', ' ')}</b>:</div>
                <div class="code">{code}</div>
                <div class="footer">If you did not request this, you can ignore this email.</div>
            </div>
        </body>
        </html>
        """
        self.yag.send(
            to=self.sender,
            subject=self.subject,
            contents=[body],
        )

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.db import db


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, username, email, password=None, is_active_user=True, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.is_active_user = is_active_user
        if password:
            self.set_password(password)

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<AdminUser {self.username}>"

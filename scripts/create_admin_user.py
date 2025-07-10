#!/usr/bin/env python3
"""
Script to create the first admin user for the Student Course Advising System
"""

from dotenv import load_dotenv

load_dotenv()

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.admin_user import AdminUser
from app.core.db import db
from config.settings import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL


def create_admin_user():
    app = create_app()

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Check if admin user already exists
        existing_admin = AdminUser.query.filter_by(username=ADMIN_USERNAME).first()

        if existing_admin:
            print(f"Admin user '{ADMIN_USERNAME}' already exists!")
            return

        # Create new admin user
        admin_user = AdminUser(username=ADMIN_USERNAME, email=ADMIN_EMAIL)
        admin_user.set_password(ADMIN_PASSWORD)

        try:
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
            print(f"Username: {ADMIN_USERNAME}")
            print(f"Password: {ADMIN_PASSWORD}")
            print(f"Email: {ADMIN_EMAIL}")
            print("\nYou can now login at: http://localhost:5000/admin/login")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")


if __name__ == "__main__":
    create_admin_user()

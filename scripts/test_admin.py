#!/usr/bin/env python3
"""
Test script to verify the admin system is working correctly
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


def test_admin_system():
    app = create_app()

    with app.app_context():
        print("Testing Admin System...")

        # Test 1: Check if tables can be created
        try:
            db.create_all()
            print("✓ Database tables created successfully")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            return

        # Test 2: Check if AdminUser model works
        try:
            admin_count = AdminUser.query.count()
            print(f"✓ AdminUser model works (current count: {admin_count})")
        except Exception as e:
            print(f"✗ Error with AdminUser model: {e}")
            return

        # Test 3: Create a test admin user
        try:
            test_admin = AdminUser(username="testadmin", email="test@example.com")
            test_admin.set_password("testpass")
            db.session.add(test_admin)
            db.session.commit()
            print("✓ Test admin user created successfully")

            # Clean up
            db.session.delete(test_admin)
            db.session.commit()
            print("✓ Test admin user cleaned up")
        except Exception as e:
            print(f"✗ Error creating test admin: {e}")
            db.session.rollback()
            return

        print("\n🎉 All tests passed! The admin system is working correctly.")
        print("\nTo get started:")
        print("1. Run: python scripts/create_admin_user.py")
        print("2. Start the server: python run.py")
        print("3. Visit: http://localhost:5000/admin/login")
        print(f"4. Login with: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    test_admin_system()

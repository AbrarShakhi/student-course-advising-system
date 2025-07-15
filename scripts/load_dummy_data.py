#!/usr/bin/env python3
"""
Script to loads dummy data into the Student Course Advising System
"""

from dotenv import load_dotenv

load_dotenv()

import os
import sys
import json
from datetime import datetime, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.core.db import db
from app.models.base import CreditPart, Room, season, Timeslot, Year, Department, University
from app.models.admin_user import AdminUser
from app.models.courses import Course
from app.models.faculties import Faculty
from app.models.sections import Section, Takes, Offers
from app.models.students import Student, StudentImage, StudentLogin, StudentOTP

# Table insert order: no FKs first, then those with FKs, etc.
INSERT_ORDER = [
    ("credit_part", CreditPart),
    ("room", Room),
    ("season", season),
    ("timeslot", Timeslot),
    ("year", Year),
    ("department", Department),
    # ("admin_user", AdminUser),
    ("course", Course),
    ("faculty", Faculty),
    ("student", Student),
    # ("student_image", StudentImage),
    # ("student_login", StudentLogin),
    # ("student_otp", StudentOTP),
    ("university", University),
    ("section", Section),
    ("takes", Takes),
    ("offers", Offers),
]

def parse_time(val):
    if val is None:
        return None
    if isinstance(val, time):
        return val
    try:
        return datetime.strptime(val, "%H:%M:%S").time()
    except Exception:
        return val

def parse_datetime(val):
    if val is None:
        return None
    try:
        return datetime.fromisoformat(val)
    except Exception:
        return val

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        with open(os.path.join(os.path.dirname(__file__), "dummy_data.json")) as f:
            data = json.load(f)
        for table, model in INSERT_ORDER:
            rows = data.get(table, [])
            for row in rows:
                # Convert datetime and time fields
                for k, v in row.items():
                    if k.endswith("_time"):
                        row[k] = parse_time(v)
                    elif "date" in k or "at" in k:
                        row[k] = parse_datetime(v)
                try:
                    obj = model(**row)
                    db.session.add(obj)
                    print(f"Inserted into {table}: {row}")
                except Exception as e:
                    print(f"Error inserting into {table}: {row}\n{e}")
        try:
            db.session.commit()
            print("All dummy data inserted successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing data: {e}")

if __name__ == "__main__":
    main() 
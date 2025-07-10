from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from functools import wraps


def init_admin(app, db):
    admin = Admin(
        app, name="Student Course Advising System", template_mode="bootstrap4"
    )

    # Import models
    from app.models.students import Student, StudentImage, StudentLogin, StudentOTP
    from app.models.courses import Course
    from app.models.base import (
        CreditPart,
        Room,
        season,
        Timeslot,
        University,
        Year,
        Department,
    )
    from app.models.sections import Section, Takes, Offers
    from app.models.faculties import Faculty
    from app.models.admin_user import AdminUser

    # Secure ModelView that requires admin login
    class SecureModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated and hasattr(current_user, "id")

        def inaccessible_callback(self, name, **kwargs):
            from flask import redirect, url_for

            return redirect(url_for("admin_auth.admin_login"))

    # Add model views to admin
    admin.add_view(SecureModelView(Student, db.session, name="Students"))
    admin.add_view(SecureModelView(StudentImage, db.session, name="Student Images"))
    admin.add_view(SecureModelView(StudentLogin, db.session, name="Student Logins"))
    admin.add_view(SecureModelView(StudentOTP, db.session, name="Student OTPs"))
    admin.add_view(SecureModelView(Course, db.session, name="Courses"))
    admin.add_view(SecureModelView(CreditPart, db.session, name="Credit Parts"))
    admin.add_view(SecureModelView(Room, db.session, name="Rooms"))
    admin.add_view(SecureModelView(season, db.session, name="Seasons"))
    admin.add_view(SecureModelView(Timeslot, db.session, name="Timeslots"))
    admin.add_view(SecureModelView(University, db.session, name="University"))
    admin.add_view(SecureModelView(Year, db.session, name="Years"))
    admin.add_view(SecureModelView(Department, db.session, name="Departments"))
    admin.add_view(SecureModelView(Section, db.session, name="Sections"))
    admin.add_view(SecureModelView(Takes, db.session, name="Takes"))
    admin.add_view(SecureModelView(Offers, db.session, name="Offers"))
    admin.add_view(SecureModelView(Faculty, db.session, name="Faculties"))
    admin.add_view(SecureModelView(AdminUser, db.session, name="Admin Users"))

    return admin

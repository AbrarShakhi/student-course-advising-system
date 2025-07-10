from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from functools import wraps
from wtforms import StringField, IntegerField


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

    # Inline admin classes
    class StudentModelView(SecureModelView):
        pass  # No inlines for one-to-one models

    class SectionModelView(SecureModelView):
        pass  # No inlines for composite key models

    class FacultyModelView(SecureModelView):
        pass  # No inlines for composite key models

    class EditablePKModelView(ModelView):
        can_edit = True
        can_create = True
        can_delete = True
        form_excluded_columns = []

        def __init__(self, model, session, **kwargs):
            super().__init__(model, session, **kwargs)
            self.form_columns = [c.name for c in model.__table__.columns]

        def scaffold_form(self):
            form_class = super().scaffold_form()
            # Force PK fields to be editable
            for col in self.model.__table__.columns:
                if col.primary_key:
                    if hasattr(form_class, col.name):
                        # Remove existing field if present
                        delattr(form_class, col.name)
                    if col.type.python_type == int:
                        setattr(form_class, col.name, IntegerField(col.name))
                    else:
                        setattr(form_class, col.name, StringField(col.name))
            # Remove readonly from PK and FK fields if set
            for name, field in form_class.__dict__.items():
                if hasattr(field, "widget") and hasattr(field.widget, "input_type"):
                    field.widget.input_type = "text"
                if hasattr(field, "flags") and hasattr(field.flags, "readonly"):
                    field.flags.readonly = False
            return form_class

    # Add model views to admin
    admin.add_view(EditablePKModelView(Student, db.session, name="Students"))
    admin.add_view(EditablePKModelView(StudentImage, db.session, name="Student Images"))
    admin.add_view(EditablePKModelView(StudentLogin, db.session, name="Student Logins"))
    admin.add_view(EditablePKModelView(StudentOTP, db.session, name="Student OTPs"))
    admin.add_view(EditablePKModelView(Course, db.session, name="Courses"))
    admin.add_view(EditablePKModelView(CreditPart, db.session, name="Credit Parts"))
    admin.add_view(EditablePKModelView(Room, db.session, name="Rooms"))
    admin.add_view(EditablePKModelView(season, db.session, name="Seasons"))
    admin.add_view(EditablePKModelView(Timeslot, db.session, name="Timeslots"))
    admin.add_view(EditablePKModelView(University, db.session, name="University"))
    admin.add_view(EditablePKModelView(Year, db.session, name="Years"))
    admin.add_view(EditablePKModelView(Department, db.session, name="Departments"))
    admin.add_view(EditablePKModelView(Section, db.session, name="Sections"))
    admin.add_view(EditablePKModelView(Takes, db.session, name="Takes"))
    admin.add_view(EditablePKModelView(Offers, db.session, name="Offers"))
    admin.add_view(EditablePKModelView(Faculty, db.session, name="Faculties"))
    admin.add_view(EditablePKModelView(AdminUser, db.session, name="Admin Users"))
    return admin

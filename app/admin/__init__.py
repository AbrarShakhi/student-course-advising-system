from app.admin.crud_routes import generate_crud_routes
from app.models.admin_user import AdminUser
from app.models.base import (
    CreditPart,
    Room,
    Season,
    Timeslot,
    University,
    Year,
    Department,
)
from app.models.courses import Course, StudentChoices
from app.models.faculties import Faculty
from app.models.sections import Section, Takes, Offers
from app.models.students import Student, StudentImage, StudentLogin, StudentOTP


def register_crud_blueprints(app):
    models = [
        AdminUser,
        CreditPart,
        Room,
        Season,
        Timeslot,
        University,
        Year,
        Department,
        Course,
        StudentChoices,
        Faculty,
        Section,
        Takes,
        Offers,
        Student,
        StudentImage,
        StudentLogin,
        StudentOTP,
    ]

    for model in models:
        bp = generate_crud_routes(model, f"{model.__tablename__}_bp")
        app.register_blueprint(bp, url_prefix=f"/admin/{model.__tablename__}")

from re import S
from flask import current_app

from app.core.db import save_db, db, SQLAlchemyError
from app.core.responses import invalid_value, missing_fields
from app.models import Student, University, Year, Season, StudentChoices
from app.core.serializers.base import (
    serialize_semester,
    serialize_university,
)
from app.core.utils.long_query import (
    fetch_schedule,
    fetch_elegiable_courses,
    fetch_chosen_course,
)


def list_semesters_controller():
    years = Year.query.order_by(Year.year.desc()).all()
    seasons = Season.query.order_by(Season.season_id).all()
    semesters = [serialize_semester(y, s) for y in years for s in seasons]
    return {"semesters": semesters}, 200


def university_info_controller():
    uni_info: University | None = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(
            f"[AUDIT] In database table:'university | Credit_part' error."
        )
        raise Exception
    return serialize_university(uni_info), 200


def class_schedule_controller(student: Student, season_id, year):

    if not all([season_id, year]):
        return missing_fields(["season_id", "year"])

    try:
        season_id_int = int(season_id)
        year_int = int(year)
    except (TypeError, ValueError):
        return invalid_value([season_id, year])

    return {
        "schedule": [
            {
                "course_id": row.course_id,
                "section_no": row.section_no,
                "room_no": row.room_no,
                "day": row.day,
                "start_time": str(row.start_time),
                "end_time": str(row.end_time),
                "faculty_short_id": row.faculty_short_id,
            }
            for row in fetch_schedule(student, season_id_int, year_int)
        ]
    }, 200


def list_courses_controller(student: Student):
    return {
        "courses": [
            {
                "course_id": row.course_id,
                "course_title": row.title,
                "course_credit": row.credit,
            }
            for row in fetch_elegiable_courses(student)
        ]
    }, 200


def list_chosen_courses_controller(student: Student, season_id, year):
    if not all([season_id, year]):
        return missing_fields(["season_id", "year"])

    try:
        season_id_int = int(season_id)
        year_int = int(year)
    except (TypeError, ValueError):
        return invalid_value([season_id, year])

    return {
        "chosen_courses": [{"course_id": row.course_id}]
        for row in fetch_chosen_course(student, season_id_int, year_int)
    }


def select_course_controler(student: Student, course_id):
    if not all([course_id]):
        return missing_fields(["course_id"])

    uni_info = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(
            f"[AUDIT] In database table:'university | Credit_part' error."
        )
        raise Exception

    if course_id in fetch_chosen_course(
        student, uni_info.curr_season, uni_info.curr_year
    ):
        return {"message": "You already selected this course."}, 401

    if course_id not in fetch_elegiable_courses(student):
        return {"message": "You are not eligiable for this course."}, 401

    std_choise = StudentChoices(
        student_id=student.student_id,  # type: ignore
        course_id=course_id,  # type: ignore
        year=uni_info.curr_year,  # type: ignore
        season_id=uni_info.curr_season,  # type: ignore
    )
    if save_db(std_choise) is False:
        return {"message": "Unable to select course."}, 401
    return {"message": "Course selected."}, 200


def deselect_course_controler(student: Student, course_id):
    if not all([course_id]):
        return missing_fields(["course_id"])

    uni_info = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(
            f"[AUDIT] In database table:'university | Credit_part' error."
        )
        raise Exception

    student_choice = StudentChoices.query.filter_by(
        student_id=student.student_id,
        course_id=course_id,
        season_id=uni_info.curr_season,
        year=uni_info.curr_year,
    ).first()

    if not student_choice:
        return {"message": "You did not choose this course."}, 401

    try:
        db.session.delete(student_choice)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "Unable to select the course."}, 401

    return {"message": "Course dropped."}, 200

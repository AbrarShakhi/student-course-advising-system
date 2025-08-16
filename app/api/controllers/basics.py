from flask import current_app

from app.core.responses import internal_server_error, invalid_value, missing_fields
from app.core.utils.std_manager import valid_str_req_value
from app.core.db import db
from app.models import Student, University, Year, Season, Takes, Section, Offers, Course
from app.core.serializers.base import (
    serialize_semester,
    serialize_university,
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

    results = (
        db.session.query(
            Takes.course_id,
            Takes.section_no,
            Section.room_no,
            Section.day,
            Section.start_time,
            Section.end_time,
            Offers.faculty_short_id,
        )
        .join(
            Section,
            (Takes.season_id == Section.season_id)
            & (Takes.year == Section.year)
            & (Takes.section_no == Section.section_no)
            & (Takes.course_id == Section.course_id),
        )
        .join(
            Offers,
            (Takes.season_id == Offers.season_id)
            & (Takes.year == Offers.year)
            & (Takes.section_no == Offers.section_no)
            & (Takes.course_id == Offers.course_id),
        )
        .filter(
            Takes.student_id == student.student_id,
            Takes.season_id == season_id_int,
            Takes.year == year_int,
        )
        .all()
    )

    schedule = [
        {
            "course_id": row.course_id,
            "section_no": row.section_no,
            "room_no": row.room_no,
            "day": row.day,
            "start_time": str(row.start_time),
            "end_time": str(row.end_time),
            "faculty_short_id": row.faculty_short_id,
        }
        for row in results
    ]

    return {"schedule": schedule}, 200


def list_courses_controller(student: Student, season_id, year):
    if not all([season_id, year]):
        return missing_fields(["season_id", "year"])

    Course.query.filter_by()
    return internal_server_error()

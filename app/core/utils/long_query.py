from sqlalchemy import or_

from app.core.db import db
from app.models import Student, StudentChoices, Takes, Section, Offers, Course


def fetch_schedule(student: Student, season_id_int: int, year_int: int):
    return (
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


def fetch_eligible_courses(student: Student):
    passed_course_ids_subq = (
        db.session.query(Takes.course_id)
        .filter(
            Takes.student_id == student.student_id,
            Takes.grade > 0,
            Takes.is_dropped == False,
        )
        .subquery()
    )

    return (
        db.session.query(Course.course_id, Course.title, Course.credit)
        .filter(
            Course.need_credit <= student.credit_completed,
            Course.dept_id == student.dept_id,
            or_(
                Course.prerequisite_id == None,
                Course.prerequisite_id.in_(
                    db.session.query(passed_course_ids_subq.c.course_id)
                ),
            ),
        )
        .all()
    )


def fetch_chosen_course(student: Student, season_id_int: int, year_int: int):
    return StudentChoices.query.filter_by(
        student_id=student.student_id, season_id=season_id_int, year=year_int
    ).all()

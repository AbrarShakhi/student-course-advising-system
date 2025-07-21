from typing import Any, Literal

from flask import current_app

from app.models import University, Year, Season
from app.core.serializers.base import (
    serialize_semester,
    serialize_university,
)


def list_semesters_controller() -> tuple[dict[str, list[dict[str, Any]]], Literal[200]]:
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


def class_schedule_controller(student):
    return {}, 500

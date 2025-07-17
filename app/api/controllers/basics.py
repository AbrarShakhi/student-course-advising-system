from flask import current_app

from app.models.base import Year, season, University, CreditPart
from app.core.serializers.base import (
    serialize_semester,
    serialize_university,
    serialize_credit_partition,
)


def list_semesters_controller():
    years = Year.query.order_by(Year.year.desc()).all()
    seasons = season.query.order_by(season.season_id).all()
    semesters = [serialize_semester(y, s) for y in years for s in seasons]
    return {"semesters": semesters}, 200


def university_info_controller():
    uni_info = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(f"[AUDIT] In database table:'university' error.")
        raise Exception

    return serialize_university(uni_info), 200


def credit_partition_controller():
    return {
        "partitions": [
            serialize_credit_partition(part) for part in CreditPart.query.all()
        ]
    }, 200

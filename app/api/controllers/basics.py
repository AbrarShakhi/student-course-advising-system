from flask import current_app
from app.models.base import Year, season
from app.models.base import University
from app.core.serializers.base import serialize_semester, serialize_university


def list_semesters_controller():
    years = Year.query.order_by(Year.year.desc()).all()
    seasons = season.query.order_by(season.season_id).all()
    semesters = [serialize_semester(y, s) for y in years for s in seasons]
    return {"semesters": semesters}, 200


def university_info_controller():
    uni_info = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(f"[AUDIT] In database table:'university' error.")

    return serialize_university(uni_info), 200

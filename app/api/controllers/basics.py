from app.models.base import Year, season
from app.core.serializers.base import (
    serialize_semester,
    serialize_university,
)
from app.core.utils.helpers import get_uni_info


def list_semesters_controller():
    years = Year.query.order_by(Year.year.desc()).all()
    seasons = season.query.order_by(season.season_id).all()
    semesters = [serialize_semester(y, s) for y in years for s in seasons]
    return {"semesters": semesters}, 200


def university_info_controller():
    uni_info = get_uni_info()
    return serialize_university(uni_info), 200


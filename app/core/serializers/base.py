from typing import Any

from app.models import University, Year, Season, CreditPart


def serialize_semester(year: Year, season: Season) -> dict[str, Any]:
    return {
        "year": year.year,
        "season_id": season.season_id,
        "season_name": season.season_name,
    }


def serialize_credit_partition(credit_part: CreditPart) -> dict[str, Any]:
    return {
        "credit_id": credit_part.credit_id,
        "min_cred": credit_part.min_cred,
        "max_cred": credit_part.max_cred,
    }


def serialize_university(university: University) -> dict[str, Any]:
    return {
        "option": university.option,
        "is_advising": university.is_advising,
        "curr_season": university.curr_season,
        "curr_year": university.curr_year,
        "credit_id": university.credit_id,
        "min_cred_need": university.min_cred_need,
        "max_cred_need": university.max_cred_need,
    }

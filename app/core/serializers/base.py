def serialize_semester(year, season):
    return {
        "year": year.year,
        "season_id": season.season_id,
        "season_name": season.season_name,
    }


def serialize_university(university):
    return {
        "option": university.option,
        "is_advising": university.is_advising,
        "curr_season": university.curr_season,
        "curr_year": university.curr_year,
        "credit_id": university.credit_id,
    }

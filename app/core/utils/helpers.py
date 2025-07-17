from flask import current_app

from app.models.base import University


def get_uni_info():
    uni_info = University.query.filter_by(option=1).first()
    if uni_info is None:
        current_app.logger.error(f"[AUDIT] In database table:'university' error.")
        raise Exception

    return uni_info

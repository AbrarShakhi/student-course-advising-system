from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def save_db(model):
    try:
        db.session.add(model)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return False

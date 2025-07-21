from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db: SQLAlchemy = SQLAlchemy()


def save_db(model) -> bool:
    try:
        db.session.add(model)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

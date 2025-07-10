from app.models.db import db

# -----------------------------
# CreditPart Model
# -----------------------------
class CreditPart(db.Model):
    __tablename__ = 'credit_part'
    credit_id = db.Column(db.SmallInteger, primary_key=True)
    min = db.Column(db.SmallInteger, unique=True, nullable=False)
    max = db.Column(db.SmallInteger, unique=True, nullable=False)

# -----------------------------
# Room Model
# -----------------------------
class Room(db.Model):
    __tablename__ = 'room'
    room_no = db.Column(db.String(7), primary_key=True)
    building = db.Column(db.String(256), nullable=False)

# -----------------------------
# season Model
# -----------------------------
class season(db.Model):
    __tablename__ = 'season'
    season_id = db.Column(db.SmallInteger, primary_key=True)
    season_name = db.Column(db.String(10))

# -----------------------------
# Timeslot Model
# -----------------------------
class Timeslot(db.Model):
    __tablename__ = 'timeslot'
    day = db.Column(db.String(5), primary_key=True)
    start_time = db.Column(db.Time, primary_key=True)
    end_time = db.Column(db.Time, primary_key=True)

# -----------------------------
# University Model
# -----------------------------
class University(db.Model):
    __tablename__ = 'university'
    option = db.Column(db.SmallInteger, primary_key=True)
    is_advising = db.Column(db.Boolean)
    curr_season = db.Column(db.SmallInteger, db.ForeignKey('season.season_id'), nullable=False)
    curr_year = db.Column(db.SmallInteger, db.ForeignKey('year.year'), nullable=False)
    credit_id = db.Column(db.SmallInteger, db.ForeignKey('credit_part.credit_id'), nullable=False)

    season = db.relationship('season', backref='universities')
    year_rel = db.relationship('Year', backref='universities')
    credit_part = db.relationship('CreditPart', backref='universities')

# -----------------------------
# Year Model
# -----------------------------
class Year(db.Model):
    __tablename__ = 'year'
    year = db.Column(db.SmallInteger, primary_key=True)

# -----------------------------
# Department Model
# -----------------------------
class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.SmallInteger, primary_key=True)
    dept_short_name = db.Column(db.String(6), nullable=False)
    long_name = db.Column(db.String(256), nullable=False) 
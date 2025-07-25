from app.core.db import db


# -----------------------------
# Section Model
# -----------------------------
class Section(db.Model):
    __tablename__ = "section"
    season_id = db.Column(
        db.SmallInteger, db.ForeignKey("season.season_id"), primary_key=True
    )
    year = db.Column(db.SmallInteger, db.ForeignKey("year.year"), primary_key=True)
    section_no = db.Column(db.SmallInteger, primary_key=True)
    course_id = db.Column(
        db.String(6), db.ForeignKey("course.course_id"), primary_key=True
    )
    capacity = db.Column(db.SmallInteger)
    room_no = db.Column(db.String(7), db.ForeignKey("room.room_no"), nullable=False)
    day = db.Column(db.String(5), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # Composite FK to timeslot
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["day", "start_time", "end_time"],
            ["timeslot.day", "timeslot.start_time", "timeslot.end_time"],
        ),
    )

    # Relationships
    course = db.relationship("Course", backref="sections")
    room = db.relationship("Room", backref="sections")
    season = db.relationship("Season", backref="sections")
    year_rel = db.relationship("Year", backref="sections")
    timeslot = db.relationship(
        "Timeslot",
        primaryjoin="and_(Section.day==Timeslot.day, Section.start_time==Timeslot.start_time, Section.end_time==Timeslot.end_time)",
        backref="sections",
    )
    offers = db.relationship(
        "Offers", back_populates="section", cascade="all, delete-orphan"
    )
    takes = db.relationship(
        "Takes", back_populates="section", cascade="all, delete-orphan"
    )


# -----------------------------
# Takes Model
# -----------------------------
class Takes(db.Model):
    __tablename__ = "takes"
    season_id = db.Column(db.SmallInteger, primary_key=True)
    year = db.Column(db.SmallInteger, primary_key=True)
    section_no = db.Column(db.SmallInteger, primary_key=True)
    course_id = db.Column(db.String(6), primary_key=True)
    student_id = db.Column(
        db.String(13), db.ForeignKey("student.student_id"), primary_key=True
    )
    grade = db.Column(db.Numeric(4, 2), default=0.0)
    is_dropped = db.Column(db.Boolean, default=False)

    # Foreign key to section (composite)
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["season_id", "year", "section_no", "course_id"],
            [
                "section.season_id",
                "section.year",
                "section.section_no",
                "section.course_id",
            ],
        ),
    )
    section = db.relationship(
        "Section",
        back_populates="takes",
        primaryjoin="and_(Takes.season_id==Section.season_id, Takes.year==Section.year, Takes.section_no==Section.section_no, Takes.course_id==Section.course_id)",
    )
    student = db.relationship("Student", back_populates="takes")


# -----------------------------
# Offers Model
# -----------------------------
class Offers(db.Model):
    __tablename__ = "offers"
    season_id = db.Column(db.SmallInteger, primary_key=True)
    year = db.Column(db.SmallInteger, primary_key=True)
    section_no = db.Column(db.SmallInteger, primary_key=True)
    course_id = db.Column(db.String(6), primary_key=True)
    faculty_short_id = db.Column(
        db.String(10), db.ForeignKey("faculty.faculty_short_id"), primary_key=True
    )

    # Foreign key to section (composite)
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["season_id", "year", "section_no", "course_id"],
            [
                "section.season_id",
                "section.year",
                "section.section_no",
                "section.course_id",
            ],
        ),
    )
    section = db.relationship(
        "Section",
        back_populates="offers",
        primaryjoin="and_(Offers.season_id==Section.season_id, Offers.year==Section.year, Offers.section_no==Section.section_no, Offers.course_id==Section.course_id)",
    )
    faculty = db.relationship("Faculty", back_populates="offers")

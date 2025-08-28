from app.core.db import db


# -----------------------------
# Course Model
# -----------------------------
class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.String(6), primary_key=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    credit = db.Column(db.Numeric(2, 1), nullable=False)
    need_credit = db.Column(db.Numeric(4, 1), nullable=False, default=0)
    amount = db.Column(db.Numeric(10, 4), nullable=False)
    prerequisite_id = db.Column(
        db.String(6), db.ForeignKey("course.course_id"), nullable=True
    )
    extra_course_id = db.Column(
        db.String(6), db.ForeignKey("course.course_id"), nullable=True
    )
    dept_id = db.Column(
        db.SmallInteger, db.ForeignKey("department.dept_id"), nullable=False
    )

    # Relationships
    prerequisite = db.relationship(
        "Course",
        remote_side=[course_id],
        foreign_keys=[prerequisite_id],
        backref="prerequisite_for",
    )
    extra_course = db.relationship(
        "Course",
        remote_side=[course_id],
        foreign_keys=[extra_course_id],
        backref="extra_for",
    )
    department = db.relationship("Department", backref="courses")
    student_choices = db.relationship(
        "StudentChoices", back_populates="course", cascade="all, delete-orphan"
    )


# -----------------------------
# StudentChoices Model
# -----------------------------
class StudentChoices(db.Model):
    __tablename__ = "student_choices"

    student_id = db.Column(
        db.String(13),
        db.ForeignKey("student.student_id"),
        primary_key=True,
        nullable=False,
    )
    course_id = db.Column(
        db.String(6),
        db.ForeignKey("course.course_id"),
        primary_key=True,
    )
    year = db.Column(
        db.SmallInteger, db.ForeignKey("year.year"), primary_key=True, nullable=False
    )
    season_id = db.Column(
        db.SmallInteger,
        db.ForeignKey("season.season_id"),
        primary_key=True,
        nullable=False,
    )

    # Relationships
    student = db.relationship("Student", back_populates="choices")
    course = db.relationship("Course", back_populates="student_choices")
    # year_rel = db.relationship("Year", back_populates="student_choices")
    # season = db.relationship("Season", back_populates="student_choices")

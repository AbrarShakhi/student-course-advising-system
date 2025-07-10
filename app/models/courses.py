from app.core.db import db


# -----------------------------
# Course Model
# -----------------------------
class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.String(6), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    credit = db.Column(db.Numeric(2, 1), nullable=False)
    need_credit = db.Column(db.Numeric(4, 1), nullable=False, default=0)
    amount = db.Column(db.Numeric(10, 4), nullable=False)
    prerequisite_id = db.Column(
        db.String(6), db.ForeignKey("course.course_id"), nullable=False
    )
    extra_course_id = db.Column(
        db.String(6), db.ForeignKey("course.course_id"), nullable=False
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

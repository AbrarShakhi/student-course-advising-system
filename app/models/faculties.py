from app.core.db import db


# -----------------------------
# Faculty Model
# -----------------------------
class Faculty(db.Model):
    __tablename__ = "faculty"
    faculty_short_id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128))
    fac_email = db.Column(db.String(128), nullable=False, unique=True)
    room_no = db.Column(db.String(7), nullable=False, unique=True)
    dept_id = db.Column(
        db.SmallInteger, db.ForeignKey("department.dept_id"), nullable=False
    )

    department = db.relationship("Department", backref="faculties")
    offers = db.relationship(
        "Offers", back_populates="faculty", cascade="all, delete-orphan"
    )

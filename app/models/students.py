from app.models.db import db

# -----------------------------
# Student Model
# -----------------------------
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.String(13), primary_key=True, unique=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128))
    mobile_no = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    is_dismissed = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(128), nullable=False)
    gardian_name = db.Column(db.String(128), nullable=False)
    gardian_phone = db.Column(db.String(128), nullable=False)
    is_graduated = db.Column(db.Boolean, nullable=False, default=False)
    credit_completed = db.Column(db.Numeric(4, 1), nullable=False, default=0)
    dept_id = db.Column(db.SmallInteger, db.ForeignKey('department.dept_id'), nullable=False)

    department = db.relationship('Department', backref='students')
    image = db.relationship('StudentImage', uselist=False, back_populates='student', cascade='all, delete-orphan')
    login = db.relationship('StudentLogin', uselist=False, back_populates='student', cascade='all, delete-orphan')
    otp = db.relationship('StudentOTP', uselist=False, back_populates='student', cascade='all, delete-orphan')
    takes = db.relationship('Takes', back_populates='student', cascade='all, delete-orphan')

# -----------------------------
# StudentImage Model
# -----------------------------
class StudentImage(db.Model):
    __tablename__ = 'student_image'
    student_id = db.Column(db.String(13), db.ForeignKey('student.student_id'), primary_key=True)
    file_name = db.Column(db.Text)
    file_data = db.Column(db.LargeBinary)

    student = db.relationship('Student', back_populates='image')

# -----------------------------
# StudentLogin Model
# -----------------------------
class StudentLogin(db.Model):
    __tablename__ = 'student_login'
    student_id = db.Column(db.String(13), db.ForeignKey('student.student_id'), primary_key=True)
    password = db.Column(db.String(128))

    student = db.relationship('Student', back_populates='login')

# -----------------------------
# StudentOTP Model
# -----------------------------
class StudentOTP(db.Model):
    __tablename__ = 'student_otp'
    student_id = db.Column(db.String(13), db.ForeignKey('student.student_id'), primary_key=True)
    otp = db.Column(db.String(6))
    created_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    try_count = db.Column(db.SmallInteger, default=0)

    student = db.relationship('Student', back_populates='otp') 
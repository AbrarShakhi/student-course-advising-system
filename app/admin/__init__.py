from flask_admin import Admin


def init_admin(app, db) -> Admin:
    admin = Admin(
        app, name="Student Course Advising System", template_mode="bootstrap4"
    )
    return admin

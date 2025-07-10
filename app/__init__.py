from flask import Flask
from app.models import db
from app.admin import init_admin
from flask_login import LoginManager
from app.models.admin_user import AdminUser
from app.admin.views import admin_auth
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

    db.init_app(app)
    init_admin(app, db)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin_auth.admin_login'

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # Register admin login/logout blueprint
    app.register_blueprint(admin_auth)

    # Register blueprints here if you have any
    # from app.api import api_bp
    # app.register_blueprint(api_bp)

    return app
